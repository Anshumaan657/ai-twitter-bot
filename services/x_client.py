import requests
from config import X_BEARER_TOKEN
from services.logger import logger

BASE_URL = "https://api.twitter.com/2"


def post_tweet(text: str):
    """
    Post tweet to X (Twitter).
    """

    url = f"{BASE_URL}/tweets"

    headers = {
        "Authorization": f"Bearer {X_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers
        )

        data = response.json()

        logger.info(f"X API response: {data}")

        return data

    except Exception as e:
        logger.error(f"X post failed: {e}")
        return None