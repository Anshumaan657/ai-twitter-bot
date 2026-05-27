import threading

from config import TELEGRAM_CHAT_ID
from services.logger import logger

from services.news_fetcher import fetch_all_ai_news
from services.tweet_generator import generate_tweets
from services.tweet_validator import validate_tweet, score_tweet
from services.memory_filter import is_tweet_too_similar

from services.database import (
    initialize_database,
    save_tweet
)

from services.telegram_bot import (
    send_message,
    send_tweet_for_approval
)

from services.telegram_listener import start_listener
from services.posting_engine import start_posting_engine


# -----------------------------
# CONFIG
# -----------------------------
MAX_RETRIES = 3
MIN_SCORE = 5


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main():

    logger.info("AI Twitter Bot started")

    # -----------------------------
    # INIT DATABASE
    # -----------------------------
    initialize_database()

    # -----------------------------
    # START TELEGRAM LISTENER
    # -----------------------------
    threading.Thread(
        target=start_listener,
        daemon=True
    ).start()

    # -----------------------------
    # START POSTING ENGINE (NEW)
    # -----------------------------
    threading.Thread(
        target=start_posting_engine,
        daemon=True
    ).start()

    # -----------------------------
    # STARTUP MESSAGE
    # -----------------------------
    send_message(
        TELEGRAM_CHAT_ID,
        "🚀 AI Twitter Bot Online"
    )

    # -----------------------------
    # FETCH NEWS
    # -----------------------------
    articles = fetch_all_ai_news()

    if not articles:
        logger.warning("No articles found")
        return

    best_article = articles[0]

    logger.info(f"Selected article: {best_article['title']}")

    # -----------------------------
    # GENERATE TWEETS
    # -----------------------------
    scored_tweets = []

    for attempt in range(MAX_RETRIES):

        logger.info(f"Generation Attempt {attempt + 1}")

        tweets = generate_tweets(best_article)

        scored_tweets.clear()

        for tweet in tweets:

            # VALIDATION
            if not validate_tweet(tweet):
                logger.warning("Tweet rejected by validator")
                continue

            # SIMILARITY FILTER
            if is_tweet_too_similar(tweet):
                logger.warning("Tweet rejected by similarity filter")
                continue

            # SCORE
            score = score_tweet(tweet)

            scored_tweets.append({
                "tweet": tweet,
                "score": score
            })

        strong_tweets = [
            t for t in scored_tweets
            if t["score"] >= MIN_SCORE
        ]

        if strong_tweets:
            scored_tweets = strong_tweets
            logger.info(f"{len(scored_tweets)} strong tweets found")
            break

    # -----------------------------
    # FAIL CASE
    # -----------------------------
    if not scored_tweets:
        logger.warning("No valid tweets generated")
        return

    # -----------------------------
    # PICK BEST TWEET
    # -----------------------------
    best_tweet = max(scored_tweets, key=lambda x: x["score"])

    # -----------------------------
    # SAVE TO DATABASE (QUEUE FOR POSTING ENGINE)
    # -----------------------------
    tweet_id = save_tweet(
        tweet_text=best_tweet["tweet"],
        article_title=best_article["title"],
        score=best_tweet["score"]
    )

    logger.info(f"Tweet queued with ID: {tweet_id}")

    # -----------------------------
    # TELEGRAM NOTIFICATION (NO CONTROL ROLE NOW)
    # -----------------------------
    send_tweet_for_approval(
        chat_id=TELEGRAM_CHAT_ID,
        tweet_id=tweet_id,
        tweet=best_tweet["tweet"],
        score=best_tweet["score"]
    )

    logger.info("Pipeline completed successfully")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()