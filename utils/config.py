from dotenv import load_dotenv
import os

load_dotenv()

api_key_openai = os.getenv("API_KEY_OPENAI")
device = os.getenv("DEVICE", "cpu")
