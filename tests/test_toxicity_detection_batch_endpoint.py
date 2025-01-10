from fastapi.testclient import TestClient
from main import app  # Replace with the actual filename of your FastAPI app

client = TestClient(app)


def test_toxicity_detection_batch():
    payload = {
        "model_field_1": "value1",
        "model_field_2": "value2",
    }

    response = client.post("/toxicity-detection-batch", json=payload)

    assert response.status_code == 200
    assert "result" in response.json()
