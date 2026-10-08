import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3.5-flash")
    DATA_DIR = os.getenv("DATA_DIR", "data")
    OUTPUT_FILE = os.path.join(DATA_DIR, "approved_actions.json")

    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is missing. Please set it in a .env file or environment.")
