from services.logger import logger

def post_to_x(tweet_text: str):

    logger.info(
        f"SIMULATED POST:\n{tweet_text}"
    )

    print("\n")
    print("=" * 60)
    print("SIMULATED X POST")
    print("=" * 60)
    print(tweet_text)
    print("=" * 60)
    print("\n")

    return True