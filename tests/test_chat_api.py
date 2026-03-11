"""Basic API tests"""
import pytest
from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '/workspace')

from monolit import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "ok" in data or "status" in data

def test_frontend_loads():
    """Test frontend loads"""
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Assistant" in response.text

def test_paint_editor_loads():
    """Test paint editor loads"""
    response = client.get("/paint")
    assert response.status_code == 200
