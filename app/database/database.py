import os

import psycopg2
import psycopg2.extras


class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            sslmode=os.getenv("DATABASE_SSL_MODE"),
        )

    def shutdown(self):
        self.connection.close()

    def get_connection(self):
        return self.connection

    def run_query(self, query):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def run_query_with_params(self, query, params):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query, params)
        if query.lower().startswith("insert"):
            self.connection.commit()
        result = cursor.fetchall()
        cursor.close()
        return result
