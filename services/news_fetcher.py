import re
import html
import feedparser

from services.logger import logger


RSS_FEEDS = {

    # AI Industry / Startup News
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "OpenAI": "https://openai.com/news/rss.xml",
    "Hugging Face": "https://huggingface.co/blog/feed.xml",

    # ML Research / Papers
    "Google AI Blog": "https://blog.google/technology/ai/rss/",
    "BAIR Blog": "https://bair.berkeley.edu/blog/feed.xml",
    "DeepMind Blog": "https://deepmind.google/blog/rss.xml",

    # Arxiv AI/ML Papers
    "Arxiv AI": "http://export.arxiv.org/rss/cs.AI",
    "Arxiv ML": "http://export.arxiv.org/rss/cs.LG",

    # Open Source / Engineering
    "PyTorch": "https://pytorch.org/feed.xml",
}


HIGH_SIGNAL_KEYWORDS = [

    # General AI
    "ai",
    "artificial intelligence",
    "agent",
    "agents",
    "agi",
    "automation",

    # LLMs
    "llm",
    "transformer",
    "foundation model",
    "multimodal",
    "reasoning",
    "inference",
    "fine-tuning",

    # ML Specific
    "machine learning",
    "deep learning",
    "neural network",
    "training",
    "dataset",
    "benchmark",
    "evaluation",
    "supervised",
    "unsupervised",
    "reinforcement learning",
    "rlhf",

    # Infra / GPUs
    "gpu",
    "cuda",
    "nvidia",
    "optimization",

    # Open Source
    "open-source",
    "pytorch",
    "tensorflow",
    "mistral",
    "llama",

    # Companies
    "openai",
    "anthropic",
    "deepmind",
    "gemini",

    # Startups
    "startup",
    "robotics",
    "synthetic",
    "copilot",
]


LOW_SIGNAL_KEYWORDS = [
    "stock",
    "celebrity",
    "sports",
    "crypto scam",
    "gossip",
    "weather",
    "politics"
]


BONUS_KEYWORDS = [
    "open-source",
    "agent",
    "reasoning",
    "foundation model",
    "startup",
    "robotics",
    "autonomous",
    "inference",
    "benchmark",
    "multimodal",
    "rlhf",
    "training",
    "optimization"
]


def clean_html(raw_html: str) -> str:
    """
    Remove HTML tags and clean text.
    """

    clean_text = re.sub(r"<.*?>", "", raw_html)

    clean_text = html.unescape(clean_text)

    clean_text = " ".join(clean_text.split())

    return clean_text


def remove_duplicates(articles: list[dict]) -> list[dict]:
    """
    Remove duplicate articles based on title.
    """

    seen_titles = set()

    unique_articles = []

    for article in articles:

        title = article["title"].strip().lower()

        if title not in seen_titles:

            seen_titles.add(title)

            unique_articles.append(article)

    return unique_articles


def is_high_quality_article(article: dict) -> bool:
    """
    Determine whether article is valuable for tweet generation.
    """

    combined_text = (
        article["title"] + " " + article["summary"]
    ).lower()

    # Reject low-signal topics
    for keyword in LOW_SIGNAL_KEYWORDS:

        if keyword in combined_text:

            return False

    # Count high-signal keywords
    score = 0

    for keyword in HIGH_SIGNAL_KEYWORDS:

        if keyword in combined_text:

            score += 1

    return score >= 1


def calculate_article_score(article: dict) -> int:
    """
    Calculate article relevance score.
    """

    combined_text = (
        article["title"] + " " + article["summary"]
    ).lower()

    score = 0

    # Base scoring
    for keyword in HIGH_SIGNAL_KEYWORDS:

        if keyword in combined_text:

            score += 2

    # Bonus scoring
    for keyword in BONUS_KEYWORDS:

        if keyword in combined_text:

            score += 3

    return score


def fetch_rss_feed(
    source_name: str,
    feed_url: str,
    limit: int = 5
) -> list[dict]:
    """
    Fetch articles from a single RSS feed.
    """

    logger.info(f"Fetching news from {source_name}")

    feed = feedparser.parse(feed_url)

    articles = []

    for entry in feed.entries[:limit]:

        article = {
            "title": clean_html(entry.get("title", "")),
            "summary": clean_html(entry.get("summary", "")),
            "link": entry.get("link", ""),
            "source": source_name
        }

        articles.append(article)

    logger.info(f"Fetched {len(articles)} articles from {source_name}")

    return articles


def fetch_all_ai_news(limit_per_source: int = 5) -> list[dict]:
    """
    Fetch news from all configured AI/ML sources.
    """

    all_articles = []

    for source_name, feed_url in RSS_FEEDS.items():

        try:

            articles = fetch_rss_feed(
                source_name=source_name,
                feed_url=feed_url,
                limit=limit_per_source
            )

            all_articles.extend(articles)

        except Exception as e:

            logger.error(f"Failed to fetch from {source_name}: {e}")

    # Remove duplicates
    unique_articles = remove_duplicates(all_articles)

    # Filter high-quality articles
    filtered_articles = [
        article
        for article in unique_articles
        if is_high_quality_article(article)
    ]

    # Score articles
    for article in filtered_articles:

        article["score"] = calculate_article_score(article)

    # Sort articles by score
    sorted_articles = sorted(
        filtered_articles,
        key=lambda article: article["score"],
        reverse=True
    )

    logger.info(
        f"Filtered {len(sorted_articles)} high-quality articles "
        f"from {len(unique_articles)} total articles"
    )

    return sorted_articles