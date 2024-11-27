import sqlite3

class Database:
    def __init__(self,path = str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS hw(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name1 TEXT,
                    group1 INTEGER,
                    hw_num INTEGER,
                    git_rep TEXT
                )
                """
            )
    def execute_query(self, query: str, params: tuple = ()):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()

database = Database("databasefortest.sqlite")
database.create_tables()