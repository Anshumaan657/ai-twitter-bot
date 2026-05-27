import time

from services.logger import logger

from services.database import (
    get_approved_tweets_for_posting,
    mark_as_posted,
    mark_post_failed
)

from services.x_client import post_tweet


# -----------------------------
# CONFIG
# -----------------------------
POST_INTERVAL_SECONDS = 6 * 60 * 60   # 6 hours
MAX_RETRY = 3


# -----------------------------
# POSTING ENGINE LOOP
# -----------------------------
def start_posting_engine():

    logger.info("Posting engine started")

    while True:

        try:

            tweets = get_approved_tweets_for_posting(limit=5)

            if not tweets:

                logger.info("No tweets in queue")

                time.sleep(60)
                continue

            for tweet_id, tweet_text, retry_count in tweets:

                if retry_count >= MAX_RETRY:

                    logger.warning(
                        f"Tweet {tweet_id} exceeded retry limit"
                    )
                    continue

                logger.info(
                    f"Posting tweet ID: {tweet_id}"
                )

                result = post_tweet(tweet_text)

                # SUCCESS
                if result:

                    mark_as_posted(tweet_id)

                    logger.info(
                        f"Tweet {tweet_id} posted successfully"
                    )

                # FAIL
                else:

                    mark_post_failed(tweet_id)

                    logger.warning(
                        f"Tweet {tweet_id} failed posting"
                    )

            # sleep cycle
            logger.info("Sleeping for 6 hours...")

            time.sleep(POST_INTERVAL_SECONDS)

        except Exception as e:

            logger.error(f"Posting engine error: {e}")

            time.sleep(60)