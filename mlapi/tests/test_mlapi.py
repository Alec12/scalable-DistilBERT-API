import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from src.main import app


@pytest.fixture
def client():
    FastAPICache.init(InMemoryBackend())
    with TestClient(app) as c:
        yield c


def test_root_not_found(client):
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

# Test /docs endpoint (Swagger UI)
def test_docs_endpoint(client):
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

# Test /openapi.json endpoint (OpenAPI documentation)
def test_openapi_json_endpoint(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

# Test /project/health endpoint
def test_health_correct_input(client):
    response = client.get("/project/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict(client):
    data = {"text": ["I hate you.", "I love you."]}
    response = client.post(
        "/project/bulk-predict",
        json=data,
    )
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json()["predictions"], list)
    assert isinstance(response.json()["predictions"][0], list)
    assert isinstance(response.json()["predictions"][0][0], dict)
    assert isinstance(response.json()["predictions"][1][0], dict)
    assert set(response.json()["predictions"][0][0].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][0][1].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][1][0].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][1][1].keys()) == {"label", "score"}
    assert response.json()["predictions"][0][0]["label"] == "NEGATIVE"
    assert response.json()["predictions"][0][1]["label"] == "POSITIVE"
    assert response.json()["predictions"][1][0]["label"] == "POSITIVE"
    assert response.json()["predictions"][1][1]["label"] == "NEGATIVE"

def test_predict_empty_input(client):
    data = {"text": []}  # Empty input list
    response = client.post(
        "/project/bulk-predict",
        json=data,
    )
    print(response.json())
    assert response.status_code == 422  # Unprocessable Entity or a custom status code
    assert "detail" in response.json()  # Standard FastAPI error field

def test_predict_large_input(client):
    # Simulate a large batch of input texts
    data = {"text": ["This is a test sentence."] * 1000}  # 1000 repeated texts
    response = client.post(
        "/project/bulk-predict",
        json=data,
    )
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json()["predictions"], list)
    assert len(response.json()["predictions"]) == 1000  # Ensure all inputs are processed
    for prediction in response.json()["predictions"]:
        assert isinstance(prediction, list)  # Ensure predictions are nested lists
        assert isinstance(prediction[0], dict)  # Ensure individual predictions are dicts
        assert set(prediction[0].keys()) == {"label", "score"}  # Check keys


def test_predict_invalid_text_type(client):
    data = {"text": "This should be a list, not a string"}  # Invalid data type
    response = client.post(
        "/project/bulk-predict",
        json=data,
    )
    print(response.json())
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()  # FastAPI error structure
    assert response.json()["detail"][0]["loc"] == ["body", "text"]  # Location of the error
    assert "Input should be a valid list" in response.json()["detail"][0]["msg"]

def test_predict_missing_text_field(client):
    data = {}  # Missing 'text' key
    response = client.post(
        "/project/bulk-predict",
        json=data,
    )
    print(response.json())
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()  # FastAPI error structure
    assert response.json()["detail"][0]["loc"] == ["body", "text"]  # Missing 'text' key
    assert response.json()["detail"][0]["msg"] == "Field required"

