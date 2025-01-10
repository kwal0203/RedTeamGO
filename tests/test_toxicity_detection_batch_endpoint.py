from fastapi.testclient import TestClient

from utils.models import Model
from main import app

import pytest


@pytest.fixture
def client():
    return TestClient(app)


def test_toxicity_detection_batch(client):
    model_data = {
        "name": "Example Model",
        "description": "A model for detecting toxicity.",
    }
    # model_instance = Model(**model_data)

    detection_batch = {
        "model": "Due",
        "num_samples": 10,
        "random": True,
        "prompts": None,
        "topics": ["topic1", "topic2"],
    }
    response = client.post("/toxicity-detection-batch", json=detection_batch)
    assert response.status_code == 200

    # Check if the response contains the expected structure
    response_data = response.json()
    assert "result" in response_data
    assert "response" in response_data["result"]
    assert response_data["result"]["response"] == "NOT IMPLEMENTED"
