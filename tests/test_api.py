
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["model_loaded"] is True


def test_prediction_endpoint():
    response = client.post(
        "/predict",
        json={
            "cpu_usage": 25,
            "memory_usage": 40,
            "response_time_ms": 120,
            "network_traffic_mb": 30
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in ["NORMAL", "ANOMALY"]
    assert data["database_status"] == "saved"
    assert "prediction_id" in data


def test_history_endpoint():
    response = client.get("/history?limit=10")
    assert response.status_code == 200
    assert "history" in response.json()
