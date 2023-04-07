import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()


        # Create the weather_data table if it doesn't exist
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {os.getenv('TABLE_NAME')} (
                city VARCHAR(255) NOT NULL PRIMARY KEY,
                temperature FLOAT NOT NULL,
                humidity FLOAT NOT NULL
            )
        """)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
