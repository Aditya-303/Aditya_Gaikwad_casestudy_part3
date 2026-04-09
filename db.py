import mysql.connector
from contextlib import contextmanager
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)


@contextmanager
def get_db_connection():
    """
    Context manager for MySQL connections.
    Automatically closes the connection when the block exits,
    even if an exception is raised — prevents connection leaks.

    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            ...
    """
    conn = None
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            connection_timeout=10,       # fail fast if DB is unreachable
            autocommit=True,             # read-only queries; no transaction needed
        )
        yield conn
    except mysql.connector.Error as e:
        logger.error("Database connection failed: %s", e)
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()
