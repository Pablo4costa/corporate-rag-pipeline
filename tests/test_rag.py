from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_documents_endpoint_exists():
    response = client.get("/api/v1/documents")
    assert response.status_code in [200, 500]

def test_query_endpoint_exists():
    response = client.post(
        "/api/v1/query",
        json={"question": "What is the vacation policy?"}
    )
    assert response.status_code in [200, 500]