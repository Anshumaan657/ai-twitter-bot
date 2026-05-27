from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from services.database import get_recent_tweets
from services.logger import logger


# Lightweight embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


SIMILARITY_THRESHOLD = 0.88


def is_tweet_too_similar(
    new_tweet: str
) -> bool:
    """
    Compare new tweet against recent tweets.
    """

    recent_tweets = get_recent_tweets()

    if not recent_tweets:

        return False

    # Generate embeddings
    new_embedding = model.encode([new_tweet])

    old_embeddings = model.encode(recent_tweets)

    # Compare similarities
    similarities = cosine_similarity(
        new_embedding,
        old_embeddings
    )[0]

    highest_similarity = max(similarities)

    logger.info(
        f"Highest similarity score: "
        f"{highest_similarity:.2f}"
    )

    return highest_similarity >= SIMILARITY_THRESHOLD