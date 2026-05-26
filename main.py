import threading

from config import TELEGRAM_CHAT_ID

from services.logger import logger

from services.news_fetcher import (
    fetch_all_ai_news
)

from services.tweet_generator import (
    generate_tweets
)

from services.tweet_validator import (
    validate_tweet,
    score_tweet
)

from services.database import (
    initialize_database,
    save_tweet
)

from services.memory_filter import (
    is_tweet_too_similar
)

from services.telegram_bot import (
    send_message,
    send_tweet_for_approval
)

from services.telegram_listener import (
    start_listener
)


# -----------------------------
# CONFIG
# -----------------------------
MAX_RETRIES = 3
MIN_SCORE = 5


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main():

    logger.info(
        "AI Twitter Bot started"
    )

    # -----------------------------
    # INITIALIZE DATABASE
    # -----------------------------
    initialize_database()

    # -----------------------------
    # START TELEGRAM LISTENER
    # -----------------------------
    listener_thread = threading.Thread(
        target=start_listener,
        daemon=True
    )

    listener_thread.start()

    # -----------------------------
    # STARTUP MESSAGE
    # -----------------------------
    startup_response = send_message(
        TELEGRAM_CHAT_ID,
        "🚀 AI Twitter Bot Online"
    )

    print("\nSTARTUP RESPONSE:\n")
    print(startup_response)

    # -----------------------------
    # FETCH NEWS
    # -----------------------------
    articles = fetch_all_ai_news()

    if not articles:

        logger.warning(
            "No articles found"
        )

        return

    # -----------------------------
    # SELECT BEST ARTICLE
    # -----------------------------
    best_article = articles[0]

    print("\nBEST ARTICLE:\n")

    print(best_article["title"])

    print(
        f"Score: "
        f"{best_article['score']}"
    )

    print("-" * 60)

    # -----------------------------
    # GENERATE TWEETS
    # -----------------------------
    scored_tweets = []

    for attempt in range(MAX_RETRIES):

        logger.info(
            f"Generation Attempt "
            f"{attempt + 1}"
        )

        tweets = generate_tweets(
            best_article
        )

        scored_tweets.clear()

        for tweet in tweets:

            # VALIDATION
            if not validate_tweet(tweet):

                logger.warning(
                    "Tweet rejected by validator"
                )

                continue

            # MEMORY FILTER
            if is_tweet_too_similar(tweet):

                logger.warning(
                    "Tweet rejected by similarity filter"
                )

                continue

            # SCORE
            score = score_tweet(tweet)

            scored_tweets.append(
                {
                    "tweet": tweet,
                    "score": score
                }
            )

        # KEEP STRONG TWEETS
        strong_tweets = [

            t
            for t in scored_tweets
            if t["score"] >= MIN_SCORE
        ]

        if strong_tweets:

            scored_tweets = strong_tweets

            logger.info(
                f"{len(scored_tweets)} "
                f"strong tweets found"
            )

            break

    # -----------------------------
    # NO VALID TWEETS
    # -----------------------------
    if not scored_tweets:

        logger.warning(
            "No valid tweets generated"
        )

        print("\nNo valid tweets generated\n")

        return

    # -----------------------------
    # RANK TWEETS
    # -----------------------------
    ranked_tweets = sorted(

        scored_tweets,

        key=lambda x: x["score"],

        reverse=True
    )

    best_tweet = ranked_tweets[0]

    # -----------------------------
    # SAVE TWEET
    # -----------------------------
    tweet_id = save_tweet(

        tweet_text=best_tweet["tweet"],

        article_title=best_article["title"],

        score=best_tweet["score"]
    )

    logger.info(
        f"Tweet stored with ID: "
        f"{tweet_id}"
    )

    # -----------------------------
    # PRINT BEST TWEET
    # -----------------------------
    print("\nBEST TWEET:\n")

    print(best_tweet["tweet"])

    print("\nTWEET SCORE:\n")

    print(best_tweet["score"])

    # -----------------------------
    # SEND TO TELEGRAM
    # -----------------------------
    telegram_response = (
        send_tweet_for_approval(

            chat_id=TELEGRAM_CHAT_ID,

            tweet_id=tweet_id,

            tweet=best_tweet["tweet"],

            score=best_tweet["score"]
        )
    )

    print("\nTELEGRAM RESPONSE:\n")

    print(telegram_response)

    logger.info(
        "Pipeline completed successfully"
    )


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":

    main()