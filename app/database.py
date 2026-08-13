import psycopg

from config import Config


def get_connection():
    return psycopg.connect(
        host=Config.DATABASE_HOST,
        port=Config.DATABASE_PORT,
        dbname=Config.DATABASE_NAME,
        user=Config.DATABASE_USER,
        password=Config.DATABASE_PASSWORD,
    )
