import requests

from config import TELEGRAM_BOT_TOKEN
from services.logger import logger


BASE_URL = (
    f"https://api.telegram.org/bot"
    f"{TELEGRAM_BOT_TOKEN}"
)
print(BASE_URL)


# -----------------------------
# SIMPLE MESSAGE
# -----------------------------
def send_message(
    chat_id: str,
    text: str
):
    """
    Send Telegram message.
    """

    url = f"{BASE_URL}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    try:

        response = requests.post(
            url,
            json=payload
        )

        data = response.json()

        logger.info(
            f"Telegram send_message response: {data}"
        )

        return data

    except Exception as e:

        logger.error(
            f"send_message failed: {e}"
        )

        return None


# -----------------------------
# SEND APPROVAL MESSAGE
# -----------------------------
def send_tweet_for_approval(
    chat_id: str,
    tweet_id: int,
    tweet: str,
    score: int
):
    """
    Send tweet for approval.
    """

    url = f"{BASE_URL}/sendMessage"

    payload = {

        "chat_id": chat_id,

        "text":
        f"🔥 *Tweet Ready*\n\n"
        f"{tweet}\n\n"
        f"Score: {score}\n"
        f"Tweet ID: {tweet_id}",

        "parse_mode": "Markdown",

        "reply_markup": {

            "inline_keyboard": [

                [
                    {
                        "text": "✅ Approve",

                        "callback_data":
                        f"approve:{tweet_id}"
                    },

                    {
                        "text": "❌ Reject",

                        "callback_data":
                        f"reject:{tweet_id}"
                    }
                ],

                [
                    {
                        "text": "🔁 Regenerate",

                        "callback_data":
                        f"regenerate:{tweet_id}"
                    }
                ]
            ]
        }
    }

    try:

        response = requests.post(
            url,
            json=payload
        )

        data = response.json()

        logger.info(
            f"Telegram approval response: {data}"
        )

        return data

    except Exception as e:

        logger.error(
            f"approval message failed: {e}"
        )

        return None


# -----------------------------
# POLLING UPDATES
# -----------------------------
def get_updates(
    offset=None
):
    """
    Poll Telegram updates.
    """

    url = f"{BASE_URL}/getUpdates"

    params = {
        "timeout": 50,
        "offset": offset
    }

    try:

        response = requests.get(
            url,
            params=params
        )

        return response.json()

    except Exception as e:

        logger.error(
            f"get_updates failed: {e}"
        )

        return None


# -----------------------------
# CALLBACK PARSER
# -----------------------------
def parse_callback(
    callback_data: str
):
    """
    Parse callback actions.
    """

    if not callback_data:

        return None

    try:

        action, tweet_id = (
            callback_data.split(":")
        )

        return {
            "action": action,
            "tweet_id": int(tweet_id)
        }

    except Exception as e:

        logger.error(
            f"callback parsing failed: {e}"
        )

        return None