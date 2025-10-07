#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
middleware.py - Rate limiting & caching middleware
"""

import time
from collections import defaultdict
from typing import Dict, Any, Optional
import hashlib
import json

# ===== RATE LIMITING =====
class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)  # user_id -> [timestamps]
        self.limits = {
            "default": (60, 60),    # 60 requests per 60 seconds
            "llm": (20, 60),        # 20 LLM calls per 60 seconds
            "upload": (10, 60),     # 10 uploads per 60 seconds
            "research": (10, 300),  # 10 research per 5 minutes
        }
    
    def check_limit(self, user_id: str, endpoint_type: str = "default") -> tuple[bool, Optional[int]]:
        """
        Check if user can make request
        Returns: (allowed: bool, retry_after: Optional[int])
        """
        now = time.time()
        limit, window = self.limits.get(endpoint_type, self.limits["default"])
        
        # Clean old requests
        self.requests[user_id] = [
            ts for ts in self.requests[user_id] 
            if now - ts < window
        ]
        
        # Check limit
        if len(self.requests[user_id]) >= limit:
            oldest = min(self.requests[user_id])
            retry_after = int(window - (now - oldest)) + 1
            return False, retry_after
        
        # Add current request
        self.requests[user_id].append(now)
        return True, None
    
    def get_usage(self, user_id: str, endpoint_type: str = "default") -> Dict[str, Any]:
        """Get current usage stats"""
        now = time.time()
        limit, window = self.limits.get(endpoint_type, self.limits["default"])
        
        # Clean old
        self.requests[user_id] = [
            ts for ts in self.requests[user_id] 
            if now - ts < window
        ]
        
        current = len(self.requests[user_id])
        remaining = max(0, limit - current)
        
        return {
            "limit": limit,
            "remaining": remaining,
            "used": current,
            "window_seconds": window,
            "reset_at": int(now + window) if current > 0 else None
        }

# Global instance
rate_limiter = RateLimiter()

# ===== RESPONSE CACHE =====
class ResponseCache:
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self.cache: Dict[str, tuple[Any, float]] = {}
        self.max_size = max_size
        self.ttl = ttl  # Time to live in seconds
        self.hits = 0
        self.misses = 0
    
    def _make_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Create cache key from endpoint and params"""
        # Sort params for consistent keys
        sorted_params = json.dumps(params, sort_keys=True)
        key_str = f"{endpoint}:{sorted_params}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, endpoint: str, params: Dict[str, Any]) -> Optional[Any]:
        """Get cached response"""
        key = self._make_key(endpoint, params)
        
        if key in self.cache:
            value, timestamp = self.cache[key]
            
            # Check if expired
            if time.time() - timestamp < self.ttl:
                self.hits += 1
                return value
            else:
                # Expired, remove
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, endpoint: str, params: Dict[str, Any], value: Any):
        """Set cached response"""
        key = self._make_key(endpoint, params)
        
        # Evict oldest if full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[key] = (value, time.time())
    
    def invalidate(self, endpoint: str = None):
        """Invalidate cache for endpoint or all"""
        if endpoint:
            # Remove all keys for this endpoint
            keys_to_remove = [
                k for k in self.cache.keys() 
                if k.startswith(self._make_key(endpoint, {})[:8])
            ]
            for k in keys_to_remove:
                del self.cache[k]
        else:
            self.cache.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 2),
            "ttl_seconds": self.ttl
        }

# Global cache instances
llm_cache = ResponseCache(max_size=500, ttl=300)      # 5 min TTL for LLM
search_cache = ResponseCache(max_size=1000, ttl=600)  # 10 min for search
general_cache = ResponseCache(max_size=2000, ttl=180) # 3 min for general
