import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["models_loaded"]["tfidf"] is True
    assert data["models_loaded"]["semantic"] is True
    assert data["models_loaded"]["hybrid"] is True
    assert data["indexed_documents"] == 25657

def test_dataset_info_endpoint():
    response = client.get("/api/dataset/info")
    assert response.status_code == 200
    data = response.json()
    assert "SciDocs" in data["dataset_name"]
    assert data["corpus_statistics"]["total_documents"] == 25657

def test_models_endpoint():
    response = client.get("/api/models")
    assert response.status_code == 200
    data = response.json()
    assert len(data["models"]) == 3
    model_ids = [m["id"] for m in data["models"]]
    assert "tfidf" in model_ids
    assert "semantic" in model_ids
    assert "hybrid" in model_ids

def test_search_endpoint_tfidf():
    payload = {
        "query": "transformer neural network",
        "model": "tfidf",
        "top_k": 5
    }
    response = client.post("/api/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 5
    assert data["results"][0]["doc_id"] != ""
    assert data["results"][0]["score"] > 0

def test_search_endpoint_semantic():
    payload = {
        "query": "what is reinforcement learning?",
        "model": "semantic",
        "top_k": 5
    }
    response = client.post("/api/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 5
    assert data["results"][0]["doc_id"] != ""
    assert data["direct_answer"] is not None

def test_search_validation_empty_query():
    payload = {
        "query": "",
        "model": "semantic",
        "top_k": 5
    }
    response = client.post("/api/search", json=payload)
    assert response.status_code == 422 # Pydantic validation error for min_length=1

def test_evaluation_summary():
    response = client.get("/api/evaluation/summary")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    first = data[0]
    assert "Precision@5" in first
    assert "Recall@5" in first
    assert "MRR" in first
    assert "nDCG@10" in first
