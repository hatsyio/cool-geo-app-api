import os

import psycopg2


class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )

    def disconnect(self):
        self.connection.close()

    def refresh_connection(self):
        self.disconnect()
        self.connect()

    def get_connection(self):
        return self.connection

    def run_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def run_query_with_params(self, query, params):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result