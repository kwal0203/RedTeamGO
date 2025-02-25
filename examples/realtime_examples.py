import requests
import json


def test_realtime_toxicity():
    """
    Example of using the realtime toxicity detection endpoint.
    This endpoint is used for checking toxicity in real-time chat scenarios.
    """

    url = "http://localhost:8000/toxicity-detection-realtime"
    payload = {"prompt": "Why are you so stupid?"}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("\nRealtime Toxicity Detection Result:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error making toxicity request: {e}")


def test_realtime_bias():
    """
    Example of using the realtime bias detection endpoint.
    This endpoint is used for checking bias in real-time chat scenarios.
    """

    url = "http://localhost:8000/bias-detection-realtime"
    payload = {"prompt": "Can women be good engineers?"}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("\nRealtime Bias Detection Result:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error making bias request: {e}")


if __name__ == "__main__":
    print("Testing Realtime Detection Endpoints")
    print("===================================")

    test_realtime_toxicity()
    test_realtime_bias()
