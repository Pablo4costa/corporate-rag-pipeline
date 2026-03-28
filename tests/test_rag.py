import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_documents_empty():
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    assert "documents" in response.json()

def test_query_no_documents():
    response = client.post(
        "/api/v1/query",
        json={"question": "What is the vacation policy?"}
    )
    assert response.status_code == 200
    assert "answer" in response.json()