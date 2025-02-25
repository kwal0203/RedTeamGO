import requests
import json


def test_toxicity_batch():
    """
    Example of using the toxicity detection batch endpoint.
    This endpoint is used for offline system auditing with multiple prompts.
    """

    # API endpoint
    url = "http://localhost:8000/toxicity-detection-batch"

    # Example payload
    payload = {
        "model": {
            "name": "openai",
            "description": "GPT-4 model for toxicity testing",
            "base_url": None,
        },
        "num_samples": 5,
        "random": True,
        "database_prompts": True,
        "user_prompts": None,
        "user_topics": None,
    }

    # Headers
    headers = {"Content-Type": "application/json"}

    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)

        # Check if request was successful
        response.raise_for_status()

        # Print the response
        print("\nToxicity Batch Detection Results:")
        print(json.dumps(response.json(), indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")


if __name__ == "__main__":
    test_toxicity_batch()
