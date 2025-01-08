import os
import shutil
import subprocess
from huggingface_hub import snapshot_download


def clone_github_repos(repos):
    for repo in repos:
        tmp_dir = repo.split("/")[-1].split(".")[0] + "_tmp"
        subprocess.run(
            ["git", "clone", repo, tmp_dir],
            check=True,
        )


def download_huggingface_datasets(datasets):
    for dataset in datasets:
        print(dataset)
        snapshot_dir = snapshot_download(
            repo_id=dataset,
            repo_type="dataset",
            local_dir=dataset.split("/")[-1] + "_tmp",
        )
        print(f"Downloaded {dataset} to {snapshot_dir}")


def copy_data_files(source_dir, destination_dir, extensions=None):
    os.makedirs(destination_dir, exist_ok=True)
    extensions = extensions or []

    for root, _, files in os.walk(source_dir):
        for file in files:
            if (
                not extensions
                or any(file.endswith(ext) for ext in extensions)
                or ".jsonl" in file
            ):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(
                    destination_dir, os.path.relpath(src_path, source_dir)
                )
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)


def clean_up(temp_dir):
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"Cleaned up temporary directory: {temp_dir}")


def download_raw_data():
    github_repos = [
        "https://github.com/cuishiyao96/FFT.git",
        "https://github.com/SALT-NLP/chain-of-thought-bias.git",
        "https://github.com/AI-secure/DecodingTrust.git",
    ]
    huggingface_datasets = [
        "allenai/real-toxicity-prompts",
        "Elfsong/advpromptset",
        "lmsys/toxic-chat",
    ]
    temp_dir = "../temp"
    destination_dir = "../data"

    os.makedirs(temp_dir, exist_ok=True)
    os.chdir(temp_dir)
    clone_github_repos(github_repos)
    download_huggingface_datasets(huggingface_datasets)
    os.chdir("../scripts")

    try:
        copy_data_files(
            temp_dir, destination_dir, extensions=[".csv", ".json", ".jsonl", ".txt"]
        )
    finally:
        clean_up(temp_dir)
        print("Datasets downloaded successfully")


if __name__ == "__main__":
    download_raw_data()
