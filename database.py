import os
import mysql.connector
from dotenv import load_dotenv

from logging import configurate_logger

logger = configurate_logger()

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    logger.info("Connected to MySQL database successfully")
except mysql.connector.Error as error:
    logger.critical("Failed to connect to MySQL database")


def execute_query(query, params=None):
    try:
        if params is None:
            params = ()
        cursor.execute(query, params)
        return cursor.fetchall() if cursor.with_rows else None
    except mysql.connector.Error as err:
        logger.error(f"MySQL error {err}")


def save_language(user_id, language):
    query = """
    INSERT INTO teegram_users (user_id, language) VALUES (%s, %s) 
    ON DUBLICATE KEY UPDATE language='%s'"""
    execute_query(query, (user_id, language))


def get_statistics():
    query = """
    SELECT language, COUNT(*) as count
    from telegram_users
    GROUP BY language 
    ORDER BY count DESC"""

    return execute_query(query)
