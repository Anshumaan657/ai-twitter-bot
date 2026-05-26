from dotenv import load_dotenv
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)


print("TOKEN:", TELEGRAM_BOT_TOKEN)
print("CHAT ID:", TELEGRAM_CHAT_ID)