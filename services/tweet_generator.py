from services.gemini_service import generate_gemini_response
from services.logger import logger


def build_tweet_prompt(article: dict) -> str:
    """
    Build structured AI tweet prompt.
    """

    prompt = f"""
You are a sharp AI insider Twitter/X account.

Your task:
Generate 3 DIFFERENT tweet variations based on the article below.

STYLE:
- Modern
- Smart
- Internet-native
- Insightful
- Slightly edgy
- No emojis
- No hashtags
- No corporate tone
- No motivational fluff
- No textbook explanations

GOOD EXAMPLES:
- "AI agents are slowly turning software into coworkers instead of tools."
- "Open-source AI moves so fast that yesterday’s moat becomes today’s tutorial."
- "The most underrated AI trend is how quickly interfaces are disappearing."

RULES:
- STRICTLY under 220 characters
- Short punchy sentences
- Avoid explanations
- Avoid long setups
- Each tweet should be one compact thought
- No hashtags
- No emojis
- Output ONLY the tweets

ARTICLE:

Title:
{article['title']}

Summary:
{article['summary']}
"""

    return prompt


def shorten_tweet(tweet: str, max_length: int = 240) -> str:
    """
    Shorten tweet if too long.
    """

    if len(tweet) <= max_length:

        return tweet

    shortened = tweet[:max_length]

    # Clean cutoff
    shortened = shortened.rsplit(" ", 1)[0]

    return shortened + "..."


def clean_tweets(raw_text: str) -> list[str]:
    """
    Clean Gemini output into tweet list.
    """

    tweets = []

    lines = raw_text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove numbering
        line = line.lstrip("1234567890.- ")

        if len(line) > 20:

            shortened = shorten_tweet(line)

            tweets.append(shortened)

    return tweets


def generate_tweets(article: dict) -> list[str]:
    """
    Generate multiple AI tweet variations.
    """

    logger.info("Generating tweet variations")

    prompt = build_tweet_prompt(article)

    response = generate_gemini_response(prompt)

    tweets = clean_tweets(response)

    logger.info(f"Generated {len(tweets)} tweet variations")

    return tweets