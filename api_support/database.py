from psycopg2 import pool
from constants import USER, PASSWORD

class Database:
    connection_pool = None

    @classmethod
    def initialise(cls):
        cls.connection_pool = pool.SimpleConnectionPool(1, 10,
                                                    database='Learning',
                                                    user=USER,
                                                    password=PASSWORD,
                                                    host='localhost')
    @classmethod
    def get_connection(cls):
        return cls.connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        cls.connection_pool.putconn(connection)

    @classmethod
    def close_all_connection(cls):
        cls.connection_pool.closeall()

class CursorFromConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()

        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)

