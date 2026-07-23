import mysql.connector
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


def get_connection():

    database_url = os.getenv("MYSQL_URL")

    if database_url:
        url = urlparse(database_url)

        return mysql.connector.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path.lstrip("/"),
            port=url.port
        )

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=3306
    )