import os
from file_log import configurate_logger
import mysql.connector
from dotenv import load_dotenv

logger = configurate_logger()
load_dotenv()


def execute_query(query, params=None):
    try:
        if params is None:
            params = ()
        with mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.fetchall() if cursor.with_rows else None
    except mysql.connector.Error as err:
        logger.error(f"MySQL error: {err}")
        return None


def save_language(user_id, language):
    query = """
    INSERT INTO users (user_id, language) VALUES (%s, %s) 
    ON DUPLICATE KEY UPDATE language=%s"""
    execute_query(query, (user_id, language, language))


def get_statistics():
    query = """
    SELECT language, COUNT(*) as count
    FROM users
    GROUP BY language 
    ORDER BY count DESC"""
    return execute_query(query)