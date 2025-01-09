import sqlite3
import random


def get_random_samples(db_path, num_samples_per_dataset=10):
    """
    Retrieves random samples from the database, with an equal number from each dataset.

    Args:
      db_path: Path to the SQLite database.
      num_samples_per_dataset: Number of samples to retrieve from each dataset.

    Returns:
      A list of tuples, where each tuple contains (dataset_name, text).
      Returns an empty list if an error occurs or no data is found.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        datasets = [
            "toxic_chat",
            "advprompt",
            "real_toxicity_prompts",
            "decoding_trust",
            "fft",
            "cot_bias",
        ]
        samples = []

        for dataset in datasets:
            cursor.execute(
                "SELECT dataset, prompt FROM prompts WHERE dataset = ? ORDER BY RANDOM() LIMIT ?",
                (dataset, num_samples_per_dataset),
            )
            dataset_samples = cursor.fetchall()
            samples.extend(dataset_samples)

        conn.close()
        return samples

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []


# Example usage
db_path = "red_team_prompt_database.db"
random_samples = get_random_samples(db_path)
