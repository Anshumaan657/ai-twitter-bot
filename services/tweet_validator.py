from services.logger import logger


# Generic/cringe phrases
BANNED_PHRASES = [

    "ai is the future",
    "machine learning is",
    "artificial intelligence is",
    "changing the world",
    "revolutionary technology",
    "next level",
    "game changer",
    "leverage ai",
    "cutting-edge",
    "mind-blowing",
    "unbelievable"
]


# High-quality stylistic patterns
GOOD_PATTERNS = [

    "the real",
    "quietly",
    "slowly",
    "is becoming",
    "is turning",
    "nobody talks about",
    "the biggest shift",
    "the craziest thing",
    "feels like",
    "turning into"
]


# Weak/boring patterns
BAD_PATTERNS = [

    "in today's world",
    "it's important to",
    "businesses should",
    "ai can help",
    "this technology",
    "we can use ai"
]


def is_tweet_too_long(tweet: str) -> bool:
    """
    Check if tweet exceeds ideal length.
    """

    return len(tweet) > 240


def contains_banned_phrase(tweet: str) -> bool:
    """
    Detect low-quality generic phrases.
    """

    tweet_lower = tweet.lower()

    for phrase in BANNED_PHRASES:

        if phrase in tweet_lower:

            return True

    return False


def is_low_effort(tweet: str) -> bool:
    """
    Detect weak tweet structures.
    """

    # Too short
    if len(tweet.split()) < 8:

        return True

    # Too many emojis
    emoji_count = sum(
        1 for char in tweet
        if ord(char) > 10000
    )

    if emoji_count > 2:

        return True

    return False


def validate_tweet(tweet: str) -> bool:
    """
    Main validation pipeline.
    """

    if is_tweet_too_long(tweet):

        logger.warning("Tweet rejected: too long")

        return False

    if contains_banned_phrase(tweet):

        logger.warning("Tweet rejected: banned phrase")

        return False

    if is_low_effort(tweet):

        logger.warning("Tweet rejected: low effort")

        return False

    return True


def score_tweet(tweet: str) -> int:
    """
    Score tweet quality.
    Higher = better.
    """

    score = 0

    tweet_lower = tweet.lower()

    # Reward strong patterns
    for pattern in GOOD_PATTERNS:

        if pattern in tweet_lower:

            score += 3

    # Penalize weak patterns
    for pattern in BAD_PATTERNS:

        if pattern in tweet_lower:

            score -= 5

    # Ideal tweet length
    tweet_length = len(tweet)

    if 80 <= tweet_length <= 180:

        score += 5

    # Penalize super short tweets
    if tweet_length < 60:

        score -= 3

    # Reward punchy formatting
    if "." in tweet or ":" in tweet:

        score += 2

    return score