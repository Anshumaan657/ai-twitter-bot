from pathlib import Path
import sqlite3

from services.logger import logger


# -----------------------------
# DATABASE PATH
# -----------------------------
DB_PATH = Path("data/tweets.db")


# -----------------------------
# VALID STATES
# -----------------------------
VALID_STATUSES = [
    "generated",
    "pending",
    "approved",
    "rejected",
    "posting",
    "posted",
    "failed"
]


# -----------------------------
# CONNECTION
# -----------------------------
def get_connection():

    return sqlite3.connect(DB_PATH)


# -----------------------------
# INIT DB
# -----------------------------
def initialize_database():

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

            retry_count INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            posted_at TIMESTAMP
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

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tweets (

            tweet_text,
            article_title,
            score,
            status

        )
        VALUES (?, ?, ?, ?)
        """,
        (
            tweet_text,
            article_title,
            score,
            "approved"
        )
    )

    tweet_id = cursor.lastrowid

    connection.commit()

    connection.close()

    logger.info(
        f"Tweet saved "
        f"(queued for posting) "
        f"ID: {tweet_id}"
    )

    return tweet_id


# -----------------------------
# GET RECENT TWEETS
# -----------------------------
def get_recent_tweets(
    limit: int = 20
) -> list[str]:
    """
    Used by memory filter.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT tweet_text

        FROM tweets

        WHERE status IN (
            'approved',
            'posted'
        )

        ORDER BY created_at DESC

        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [row[0] for row in rows]


# -----------------------------
# GET APPROVED QUEUE
# -----------------------------
def get_approved_tweets_for_posting(
    limit: int = 5
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            tweet_text,
            retry_count

        FROM tweets

        WHERE status = 'approved'

        ORDER BY created_at ASC

        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


# -----------------------------
# MARK AS POSTED
# -----------------------------
def mark_as_posted(
    tweet_id: int
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tweets

        SET
            status = 'posted',
            posted_at = CURRENT_TIMESTAMP

        WHERE id = ?
        """,
        (tweet_id,)
    )

    connection.commit()

    connection.close()

    logger.info(
        f"Tweet {tweet_id} "
        f"marked as POSTED"
    )


# -----------------------------
# MARK FAILED
# -----------------------------
def mark_post_failed(
    tweet_id: int
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tweets

        SET
            status = 'failed',
            retry_count = retry_count + 1

        WHERE id = ?
        """,
        (tweet_id,)
    )

    connection.commit()

    connection.close()

    logger.warning(
        f"Tweet {tweet_id} "
        f"marked FAILED "
        f"(retry +1)"
    )


# -----------------------------
# UPDATE STATUS
# -----------------------------
def update_tweet_status(
    tweet_id: int,
    status: str
):

    if status not in VALID_STATUSES:

        logger.warning(
            f"Invalid status: {status}"
        )

        return False

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
        f"Tweet {tweet_id} -> {status}"
    )

    return True


# -----------------------------
# GET TWEET BY ID
# -----------------------------
def get_tweet_by_id(
    tweet_id: int
):

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