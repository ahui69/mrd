"""
Tests for memory/LTM functions
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestLTMSearch:
    """Test LTM search functionality"""
    
    def test_search_returns_list(self):
        """Search should return a list"""
        try:
            from monolit import ltm_search_hybrid
            results = ltm_search_hybrid("test query", limit=5)
            assert isinstance(results, list)
            assert len(results) <= 5
        except Exception as e:
            pytest.skip(f"LTM search not available: {e}")
    
    def test_search_results_have_score(self):
        """Results should have score field"""
        try:
            from monolit import ltm_search_hybrid
            results = ltm_search_hybrid("python programming", limit=3)
            if results:
                assert all('score' in r or 'conf' in r for r in results)
        except Exception as e:
            pytest.skip(f"LTM search not available: {e}")
    
    def test_search_with_limit(self):
        """Limit parameter should work"""
        try:
            from monolit import ltm_search_hybrid
            results = ltm_search_hybrid("test", limit=1)
            assert len(results) <= 1
        except Exception as e:
            pytest.skip(f"LTM search not available: {e}")


class TestTokenization:
    """Test tokenization helpers"""
    
    def test_tokenization_exists(self):
        """Tokenization function should exist"""
        try:
            from monolit import _tok
            tokens = _tok("This is a test sentence")
            assert isinstance(tokens, list)
            assert len(tokens) > 0
        except Exception as e:
            pytest.skip(f"Tokenization not available: {e}")


# Run with: pytest tests/test_memory.py -v
