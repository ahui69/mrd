"""
Pytest configuration and fixtures
"""
import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test environment variables
os.environ.setdefault("AUTH_TOKEN", "0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5")
os.environ.setdefault("DB_PATH", "data/monolit.db")

@pytest.fixture
def auth_headers():
    """Fixture providing auth headers"""
    return {
        "Authorization": f"Bearer {os.getenv('AUTH_TOKEN')}"
    }

@pytest.fixture
def sample_chat_message():
    """Fixture providing sample chat message"""
    return {
        "messages": [{"role": "user", "content": "Test message"}],
        "user_id": "test_user",
        "use_memory": False
    }

@pytest.fixture
def sample_ltm_fact():
    """Fixture providing sample LTM fact"""
    return {
        "text": "Sample fact for testing",
        "tags": ["test", "sample"],
        "source": "pytest",
        "conf": 0.8
    }
