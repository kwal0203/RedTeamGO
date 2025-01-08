import os
import glob
import shutil

source_patterns = {
    "chain_of_thought_bias": "chain-of-thought-bias_tmp/output/qa/davinci-001*.json",
    "decoding_trust": "DecodingTrust_tmp/data/toxicity/user_prompts/*.jsonl",
    "fft": "FFT_tmp/Toxicity/*.json",
    "real_toxicity_prompts": "real-toxicity-prompts_tmp/*.jsonl",
    "toxic_chat": "toxic-chat_tmp/data/0124/*.csv",
    "advprompt": "advpromptset_tmp/*.jsonl",
}


def copy_files():
    destination_base = "./"
    os.chdir("./data")
    for dataset, pattern in source_patterns.items():
        destination_dir = os.path.join(destination_base, dataset)
        os.makedirs(dataset, exist_ok=True)

        # Find and copy matching files
        source_dirs = set()
        for file_path in glob.glob(pattern):
            destination_path = (
                os.path.join(destination_dir, os.path.basename(file_path))
                .lower()
                .replace("-", "_")
            )

            exclude_keywords = [
                "gpt",
                "nontoxic",
                "davinci_001_labs.json",
                "toxic_chat_annotation_test.csv",
                "toxic_chat_annotation_train.csv",
            ]

            if any(keyword in destination_path for keyword in exclude_keywords):
                continue

            shutil.copy2(file_path, destination_path)
            source_dirs.add(os.path.dirname(file_path))

        # Remove source directories after copying files
        for source_dir in source_dirs:
            _source_dir = source_dir.split("/")[0]
            if os.path.exists(_source_dir):
                shutil.rmtree(_source_dir)
                print(f"Deleted source directory: {source_dir}")


if __name__ == "__main__":
    copy_files()
