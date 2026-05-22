from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate API key existence
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")