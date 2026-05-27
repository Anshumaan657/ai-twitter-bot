from services.logger import logger

def post_to_x(tweet_text: str):

    logger.info(
        f"SIMULATED POST:\n{tweet_text}"
    )

    print("\n====================")
    print("SIMULATED X POST")
    print("====================\n")

    print(tweet_text)

    print("\n====================\n")

    return True