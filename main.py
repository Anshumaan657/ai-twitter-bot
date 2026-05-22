from services.logger import logger
from services.news_fetcher import fetch_all_ai_news
from services.tweet_generator import generate_tweets


def main():

    logger.info("AI Twitter Bot started")

    articles = fetch_all_ai_news()

    if not articles:

        logger.warning("No articles found")

        return

    # Best article
    best_article = articles[0]

    print("\nBEST ARTICLE:\n")

    print(best_article["title"])
    print(f"Score: {best_article['score']}")
    print("-" * 80)

    # Generate tweets
    tweets = generate_tweets(best_article)

    print("\nGENERATED TWEETS:\n")

    for index, tweet in enumerate(tweets, start=1):

        print(f"{index}. {tweet}\n")


if __name__ == "__main__":
    main()