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


MAX_RETRIES = 3
MINIMUM_SCORE = 5


def main():

    logger.info("AI Twitter Bot started")
    initialize_database()

    articles = fetch_all_ai_news()

    if not articles:

        logger.warning("No articles found")

        return

    # Best ranked article
    best_article = articles[0]

    print("\nBEST ARTICLE:\n")

    print(best_article["title"])
    print(f"Score: {best_article['score']}")

    print("-" * 80)

    scored_tweets = []

    # Retry generation if tweets are weak
    for attempt in range(MAX_RETRIES):

        logger.info(f"Generation attempt {attempt + 1}")

        tweets = generate_tweets(best_article)

        scored_tweets.clear()

        # Validate + score tweets
        for tweet in tweets:

            if validate_tweet(tweet):

                score = score_tweet(tweet)

                scored_tweets.append(
                    {
                        "tweet": tweet,
                        "score": score
                    }
                )

        # Keep only strong tweets
        strong_tweets = [
            tweet
            for tweet in scored_tweets
            if tweet["score"] >= MINIMUM_SCORE
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

    # Sort best → worst
    ranked_tweets = sorted(
        scored_tweets,
        key=lambda item: item["score"],
        reverse=True
    )

    for index, item in enumerate(ranked_tweets, start=1):

        print(f"{index}. Score: {item['score']}")
        print(item["tweet"])
        print()


if __name__ == "__main__":
    main()