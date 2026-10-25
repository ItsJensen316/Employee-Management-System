import os
import mysql.connector as ms
from dotenv import load_dotenv

load_dotenv()


def connect_db():
    try:
        mydb = ms.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        return mydb

    except ms.Error as error:
        print(f"Database connection failed: {error}")
        return None