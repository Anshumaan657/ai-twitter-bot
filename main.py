from services.logger import logger

from services.news_fetcher import fetch_all_ai_news
from services.tweet_generator import generate_tweets

from services.tweet_validator import (
    validate_tweet,
    score_tweet
)

from services.database import (
    initialize_database,
    save_tweet
)

from services.memory_filter import is_tweet_too_similar

from services.telegram_bot import send_message
from config import TELEGRAM_CHAT_ID
from services.telegram_listener import start_listener

MAX_RETRIES = 3
MINIMUM_SCORE = 5


def main():

    logger.info("AI Twitter Bot started")

    # Init DB
    initialize_database()

    # Telegram test message (ONLY when bot starts)
    send_message(TELEGRAM_CHAT_ID, "Bot is now connected 🚀")

    # Fetch news
    articles = fetch_all_ai_news()

    if not articles:
        logger.warning("No articles found")
        return

    best_article = articles[0]

    print("\nBEST ARTICLE:\n")
    print(best_article["title"])
    print(f"Score: {best_article['score']}")
    print("-" * 80)

    scored_tweets = []

    # Retry loop
    for attempt in range(MAX_RETRIES):

        logger.info(f"Generation attempt {attempt + 1}")

        tweets = generate_tweets(best_article)

        scored_tweets.clear()

        for tweet in tweets:

            if not validate_tweet(tweet):
                continue

            if is_tweet_too_similar(tweet):
                logger.warning("Tweet rejected: too similar to previous tweets")
                continue

            score = score_tweet(tweet)

            scored_tweets.append({
                "tweet": tweet,
                "score": score
            })

        strong_tweets = [
            t for t in scored_tweets
            if t["score"] >= MINIMUM_SCORE
        ]

        if strong_tweets:
            logger.info("High-quality tweets generated")
            scored_tweets = strong_tweets
            break

        logger.warning("Weak tweets generated, retrying...")

    print("\nRANKED TWEETS:\n")

    if not scored_tweets:
        print("No valid tweets generated.")
        return

    ranked_tweets = sorted(
        scored_tweets,
        key=lambda item: item["score"],
        reverse=True
    )

    for i, item in enumerate(ranked_tweets, start=1):
        print(f"{i}. Score: {item['score']}")
        print(item["tweet"])
        print()

    best_tweet = ranked_tweets[0]

    save_tweet(
        tweet_text=best_tweet["tweet"],
        article_title=best_article["title"],
        score=best_tweet["score"]
    )

    print("Best tweet saved to database.")


if __name__ == "__main__":
    main()
    start_listener()