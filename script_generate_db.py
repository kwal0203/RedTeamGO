import pandas as pd
import sqlite3
import json
import re
import os


def read_jsonl(file_path):
    data = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line: {line.strip()}")
                    print(f"Error message: {e}")
                    return (
                        None  # or handle the error differently, e.g., skip the bad line
                    )
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    return data


def read_json(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)  # Load the entire file as a single JSON object
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file: {file_path}")
        print(f"Error message: {e}")
        return {}
    return data


def read_csv(file_path):
    toxic_chat = pd.read_csv(file_path)
    toxic_comments = toxic_chat[toxic_chat["toxicity"] == 1]
    user_inputs = toxic_comments["user_input"].tolist()
    return user_inputs


import os


def collect_file_paths(directory_path):
    file_paths = {"csv": [], "jsonl": [], "json": []}

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith(".csv"):
                file_paths["csv"].append(file_path)
            elif file.endswith(".jsonl"):
                file_paths["jsonl"].append(file_path)
            elif file.endswith(".json"):
                file_paths["json"].append(file_path)

    return file_paths


directory_path = "data"
file_paths = collect_file_paths(directory_path)
file_variable_mapping = {
    "advpromptset_final_10k.jsonl": "advprompt",
    "prompts.jsonl": "real_toxicity_prompts",
    "toxic.jsonl": "decoding_trust",
    "toxic_questions.json": "fft",
    "davinci_001.json": "cot_bias",
    "toxic_chat_annotation_all.csv": "toxic_chat",
}

data_store = {}
for file_path in file_paths:
    for file in file_paths[file_path]:
        filename = file.split("/")[-1]
        extension = os.path.basename(file_path)
        if filename in file_variable_mapping:
            variable_name = file_variable_mapping[filename]
            if "jsonl" in extension:
                data_store[variable_name] = read_jsonl(file)
            elif "json" in extension:
                data_store[variable_name] = read_json(file)
            elif "csv" in extension:
                data_store[variable_name] = read_csv(file)

# Data read in from json, jsonl and csv files
advprompt = data_store.get("advprompt")
real_toxicity_prompts = data_store.get("real_toxicity_prompts")
decoding_trust = data_store.get("decoding_trust")
fft = data_store.get("fft")
cot_bias = data_store.get("cot_bias")
toxic_chat = data_store.get("toxic_chat")


def clean_text_for_llama(text):
    """
    Cleans text for use with Llama models, specifically addressing potential issues.
    """
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]", "", text)

    return text


# Create database holding all red team prompts
conn = sqlite3.connect("./data/red_team_prompt_database.db")
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS prompts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset TEXT,
        prompt TEXT
    )
"""
)
conn.commit()

for i in toxic_chat:
    text = clean_text_for_llama(i)
    cursor.execute(
        "INSERT INTO prompts (dataset, prompt) VALUES (?, ?)", ("toxic_chat", text)
    )
for i in advprompt:
    text = clean_text_for_llama(i["comment_text"])
    cursor.execute(
        "INSERT INTO prompts (dataset, prompt) VALUES (?, ?)", ("advprompt", text)
    )
for i in real_toxicity_prompts:
    text = clean_text_for_llama(i["prompt"]["text"])
    cursor.execute(
        "INSERT INTO prompts (dataset, prompt) VALUES (?, ?)",
        ("real_toxicity_prompts", text),
    )
for i in decoding_trust:
    text = clean_text_for_llama(i["prompt"]["text"])
    cursor.execute(
        "INSERT INTO prompts (dataset, prompt) VALUES (?, ?)", ("decoding_trust", text)
    )
for i in fft:
    text = clean_text_for_llama(i["query"])
    cursor.execute("INSERT INTO prompts (dataset, prompt) VALUES (?, ?)", ("fft", text))
for i in cot_bias:
    text = clean_text_for_llama(cot_bias[i]["cot_prompt"])
    cursor.execute(
        "INSERT INTO prompts (dataset, prompt) VALUES (?, ?)", ("cot_bias", text)
    )

conn.commit()
conn.close()
