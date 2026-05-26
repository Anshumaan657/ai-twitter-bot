from pathlib import Path
import sqlite3

from services.logger import logger


# -----------------------------
# DATABASE PATH
# -----------------------------
DB_PATH = Path("data/tweets.db")


# -----------------------------
# CONNECTION
# -----------------------------
def get_connection():
    """
    Create SQLite connection.
    """

    return sqlite3.connect(DB_PATH)


# -----------------------------
# INITIALIZE DATABASE
# -----------------------------
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

            status TEXT DEFAULT 'pending',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()

    connection.close()

    logger.info(
        "Database initialized successfully"
    )


# -----------------------------
# SAVE TWEET
# -----------------------------
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

    tweet_id = cursor.lastrowid

    connection.commit()

    connection.close()

    logger.info(
        f"Tweet saved to database "
        f"(ID: {tweet_id})"
    )

    return tweet_id


# -----------------------------
# GET RECENT APPROVED TWEETS
# -----------------------------
def get_recent_tweets(
    limit: int = 20
) -> list[str]:
    """
    Fetch recent APPROVED tweets only.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT tweet_text

        FROM tweets

        WHERE status = 'approved'

        ORDER BY created_at DESC

        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [row[0] for row in rows]


# -----------------------------
# UPDATE TWEET STATUS
# -----------------------------
def update_tweet_status(
    tweet_id: int,
    status: str
):
    """
    Update tweet status.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tweets
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            tweet_id
        )
    )

    connection.commit()

    connection.close()

    logger.info(
        f"Tweet {tweet_id} updated to {status}"
    )


# -----------------------------
# GET TWEET BY ID
# -----------------------------
def get_tweet_by_id(
    tweet_id: int
):
    """
    Fetch single tweet by ID.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *

        FROM tweets

        WHERE id = ?
        """,
        (tweet_id,)
    )

    row = cursor.fetchone()

    connection.close()

    return row


# -----------------------------
# GET PENDING TWEETS
# -----------------------------
def get_pending_tweets():
    """
    Fetch all pending tweets.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, tweet_text, score

        FROM tweets

        WHERE status = 'pending'

        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows