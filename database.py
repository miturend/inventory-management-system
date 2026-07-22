import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()


def get_connection():

    connection = mysql.connector.connect(

        host=os.getenv("MYSQL_HOST", "127.0.0.1"),

        user=os.getenv("MYSQL_USER"),

        password=os.getenv("MYSQL_PASSWORD"),

        database=os.getenv("MYSQL_DATABASE"),

        port=3306

    )

    return connection