from dotenv import load_dotenv
import os

load_dotenv()


def get_openai_key():
    return os.getenv("API_KEY_OPENAI")


def get_device():
    return os.getenv("DEVICE", "cpu")


def get_hf_key():
    return os.getenv("HF_TOKEN")
