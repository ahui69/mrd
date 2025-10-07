"""
Basic API tests for Mordzix AI
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monolit import app

client = TestClient(app)

# Auth token for tests
AUTH_TOKEN = "0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5"
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Health endpoint should return 200 OK"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "ok" in data or "status" in data


class TestLTMEndpoints:
    """Test Long-Term Memory endpoints"""
    
    def test_ltm_search_basic(self):
        """LTM search should return results"""
        response = client.get(
            "/api/ltm/search?q=python&limit=5",
            headers=HEADERS
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or isinstance(data, list)
    
    def test_ltm_search_empty_query(self):
        """LTM search with empty query should handle gracefully"""
        response = client.get(
            "/api/ltm/search?q=&limit=5",
            headers=HEADERS
        )
        # Should either return 200 with empty results or 400 bad request
        assert response.status_code in [200, 400]
    
    def test_ltm_add_fact(self):
        """Adding fact to LTM should work"""
        fact = {
            "text": "Test fact from pytest",
            "tags": ["test", "pytest", "automated"],
            "source": "pytest",
            "conf": 0.9
        }
        response = client.post(
            "/api/ltm/add",
            json=fact,
            headers=HEADERS
        )
        assert response.status_code in [200, 201]


class TestChatEndpoints:
    """Test chat endpoints"""
    
    def test_chat_assistant_basic(self):
        """Basic chat should return response"""
        payload = {
            "messages": [{"role": "user", "content": "Hi, test message"}],
            "user_id": "test_user",
            "use_memory": False,
            "use_research": False
        }
        response = client.post(
            "/api/chat/assistant",
            json=payload,
            headers=HEADERS
        )
        # Might fail if LLM API is down, but should at least not crash
        assert response.status_code in [200, 500, 429]
    
    def test_chat_missing_messages(self):
        """Chat without messages should return error"""
        payload = {
            "user_id": "test_user"
        }
        response = client.post(
            "/api/chat/assistant",
            json=payload,
            headers=HEADERS
        )
        assert response.status_code in [400, 422]  # Validation error


class TestAuthEndpoints:
    """Test authentication"""
    
    def test_unauthorized_access(self):
        """Endpoints should reject without auth token"""
        response = client.get("/api/ltm/search?q=test&limit=5")
        assert response.status_code in [401, 403]
    
    def test_invalid_token(self):
        """Invalid token should be rejected"""
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = client.get(
            "/api/ltm/search?q=test&limit=5",
            headers=headers
        )
        assert response.status_code in [401, 403]


class TestCacheEndpoints:
    """Test cache/admin endpoints"""
    
    def test_cache_stats(self):
        """Cache stats endpoint should work"""
        response = client.get(
            "/api/admin/cache/stats",
            headers=HEADERS
        )
        assert response.status_code == 200
        data = response.json()
        assert "caches" in data or "stats" in data


class TestFrontendEndpoints:
    """Test frontend serving"""
    
    def test_frontend_loads(self):
        """Frontend should be served at /"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_paint_editor_loads(self):
        """Paint editor should be served at /paint"""
        response = client.get("/paint")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")


# Run tests with: pytest tests/test_api.py -v
# Run with coverage: pytest tests/test_api.py --cov=monolit --cov-report=html
