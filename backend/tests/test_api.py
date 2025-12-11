import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.services import RAGService
from unittest.mock import Mock, patch

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Physical AI & Humanoid Robotics Textbook Backend API"}

def test_health_endpoint():
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch('src.routers.chat.rag_service')
def test_chat_endpoint(mock_rag_service):
    """Test the chat endpoint"""
    # Mock the RAG service response
    mock_rag_service.process_query.return_value = {
        "response": "This is a test response",
        "sources": [{"title": "Test Source", "url": "/test", "relevance_score": 0.9}]
    }
    
    # Test chat request
    chat_data = {
        "message": "What is Physical AI?",
        "session_id": "test-session-123"
    }
    
    response = client.post("/api/chat", json=chat_data)
    assert response.status_code == 200
    
    response_data = response.json()
    assert "response" in response_data
    assert "sources" in response_data
    assert response_data["response"] == "This is a test response"
    assert response_data["session_id"] == "test-session-123"

@patch('src.routers.chat.rag_service')
def test_search_endpoint(mock_rag_service):
    """Test the search endpoint"""
    # Mock the RAG service search response
    mock_rag_service.search_documents.return_value = [
        {
            "content": "Test content for search result",
            "metadata": {"title": "Test Title", "url": "/test"},
            "score": 0.9
        }
    ]
    
    search_data = {
        "query": "Physical AI concepts",
        "limit": 5
    }
    
    response = client.post("/api/search", json=search_data)
    assert response.status_code == 200
    
    response_data = response.json()
    assert "results" in response_data
    assert len(response_data["results"]) == 1
    assert response_data["results"][0]["title"] == "Test Title"

def test_rate_limiting():
    """Test rate limiting functionality"""
    # This would require more complex setup to test properly
    # For now, we just verify the endpoint exists and responds appropriately
    response = client.post("/api/feedback", json={
        "session_id": "test-session",
        "message_id": "test-message",
        "rating": 1
    })
    
    # Should either succeed or fail with rate limit, but not with other errors
    assert response.status_code in [200, 429]

def test_validation_error_handling():
    """Test validation error handling"""
    # Test with empty message (should fail validation)
    response = client.post("/api/chat", json={
        "message": "",
        "session_id": "test-session-123"
    })
    
    # Should return 422 for validation error
    assert response.status_code == 422
    
    # Test with invalid session ID format (should fail validation)
    response = client.post("/api/chat", json={
        "message": "Test message",
        "session_id": "invalid session id with spaces"
    })
    
    # Should return 422 for validation error
    assert response.status_code == 422

def test_error_handling():
    """Test general error handling"""
    # Test with missing required fields
    response = client.post("/api/chat", json={})
    
    # Should return 422 for validation error due to missing fields
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main()