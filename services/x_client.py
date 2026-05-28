import tweepy
from config import (
    X_API_KEY,
    X_API_SECRET,
    X_ACCESS_TOKEN,
    X_ACCESS_SECRET
)

from services.logger import logger


# -----------------------------
# AUTH CLIENT
# -----------------------------
def get_x_client():

    try:

        auth = tweepy.OAuth1UserHandler(
            X_API_KEY,
            X_API_SECRET,
            X_ACCESS_TOKEN,
            X_ACCESS_SECRET
        )

        api = tweepy.API(auth)

        logger.info("X client initialized")

        return api

    except Exception as e:

        logger.error(f"X auth failed: {e}")
        return None


# -----------------------------
# POST TWEET
# -----------------------------
def post_tweet(text: str):

    api = get_x_client()

    if not api:
        return None

    try:

        response = api.update_status(text)

        logger.info(f"Tweet posted: {response.id}")

        return response.id

    except Exception as e:

        logger.error(f"Tweet post failed: {e}")
        return None