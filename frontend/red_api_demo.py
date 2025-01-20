import requests

# 1. Get resource:
#      sinteractive -n 1 -c 18 -g gpu:1 -m 64G -t 1:00:00 -A OD-233566
# 2. Activate conda environment
#      mini
#      conda activate tester
# 3. Run singularity script:
#      cd llama_deploy
#      ./llama3_1.sh
# 4. Run docker container for redteamgo
payload = {
    "model": {
        "name": "huggingface_llama3.1",
        "description": "Local llama3.1 model",
        "base_url": "http://localhost:8995/v1",
    },
    "num_samples": 1,
    "random": True,
    "database_prompts": True,
    "user_prompts": None,
    "user_topics": None,
}

url = "http://localhost:8995/v1/toxicity-detection-batch"
# url = "/toxicity-detection-batch"
# response = client.post("/toxicity-detection-batch", json=detection_batch)
# response_data = response.json()

response = requests.post(url, json=payload)
if response.status_code == 200:
    print("Response:", response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")
