import requests
import json


def test_bias_batch():
    """
    Example of using the bias detection batch endpoint.
    This endpoint is used for offline system auditing to detect bias in model responses.
    """

    # API endpoint
    url = "http://localhost:8000/bias-detection-batch"

    # Example payload
    payload = {
        "model": {
            "name": "gpt-4",
            "description": "GPT-4 model for bias testing",
            "base_url": None,
        },
        "prompts": {"prompt_library_path": "path/to/prompts.json"},
        "topics": ["gender", "race", "religion", "age", "disability"],
    }

    # Headers
    headers = {"Content-Type": "application/json"}

    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)

        # Check if request was successful
        response.raise_for_status()

        # Print the response
        print("\nBias Detection Batch Results:")
        print(json.dumps(response.json(), indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")


if __name__ == "__main__":
    test_bias_batch()
