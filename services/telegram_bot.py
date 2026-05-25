import requests
from config import TELEGRAM_BOT_TOKEN
from services.logger import logger

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


# -----------------------------
# BASIC MESSAGE SENDER
# -----------------------------
def send_message(chat_id: str, text: str):
    """
    Send simple Telegram message.
    """
    url = f"{BASE_URL}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        return response.json()

    except Exception as e:
        logger.error(f"Telegram send_message failed: {e}")
        return None


# -----------------------------
# SEND TWEET FOR APPROVAL
# -----------------------------
def send_tweet_for_approval(chat_id: str, tweet: str, score: int):
    """
    Sends tweet with Approve / Reject buttons.
    """

    url = f"{BASE_URL}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": f"🔥 *Tweet Ready for Approval*\n\n{tweet}\n\nScore: {score}",
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "✅ Approve",
                        "callback_data": f"approve|{score}"
                    },
                    {
                        "text": "❌ Reject",
                        "callback_data": "reject"
                    }
                ],
                [
                    {
                        "text": "🔁 Regenerate",
                        "callback_data": "regen"
                    }
                ]
            ]
        }
    }

    try:
        response = requests.post(url, json=payload)
        return response.json()

    except Exception as e:
        logger.error(f"Telegram send_tweet_for_approval failed: {e}")
        return None


# -----------------------------
# FETCH UPDATES (POLLING MODE)
# -----------------------------
def get_updates(offset=None):
    """
    Get Telegram updates (for button clicks).
    """

    url = f"{BASE_URL}/getUpdates"

    params = {
        "timeout": 100,
        "offset": offset
    }

    try:
        response = requests.get(url, params=params)
        return response.json()

    except Exception as e:
        logger.error(f"Telegram get_updates failed: {e}")
        return None


# -----------------------------
# HANDLE CALLBACK ACTIONS
# -----------------------------
def handle_callback(callback_data: str):
    """
    Parse button actions.
    """

    if not callback_data:
        return None

    if callback_data.startswith("approve"):
        _, score = callback_data.split("|")
        return {"action": "approve", "score": score}

    if callback_data == "reject":
        return {"action": "reject"}

    if callback_data == "regen":
        return {"action": "regenerate"}

    return {"action": "unknown"}