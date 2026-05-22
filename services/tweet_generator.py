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
- Maximum 240 characters each
- Each tweet must feel unique
- Focus on implications and observations
- Avoid simply summarizing the article
- Output ONLY the tweets

ARTICLE:

Title:
{article['title']}

Summary:
{article['summary']}
"""

    return prompt


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

            tweets.append(line)

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