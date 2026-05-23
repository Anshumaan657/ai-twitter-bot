import sqlite3
from pathlib import Path

from services.logger import logger


# Database path
DB_PATH = Path("data/tweets.db")


def get_connection():
    """
    Create SQLite connection.
    """

    return sqlite3.connect(DB_PATH)


def initialize_database():
    """
    Create database tables.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tweets (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            tweet_text TEXT NOT NULL,

            article_title TEXT,

            score INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()

    connection.close()

    logger.info("Database initialized successfully")


def save_tweet(
    tweet_text: str,
    article_title: str,
    score: int
):
    """
    Save generated tweet into database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tweets (
            tweet_text,
            article_title,
            score
        )
        VALUES (?, ?, ?)
        """,
        (
            tweet_text,
            article_title,
            score
        )
    )

    connection.commit()

    connection.close()

    logger.info("Tweet saved to database")


def get_recent_tweets(limit: int = 20) -> list[str]:
    """
    Fetch recent tweets.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT tweet_text
        FROM tweets
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [row[0] for row in rows]