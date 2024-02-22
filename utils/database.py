import sqlite3
from typing import List, Tuple
from utils.paths import *


class Database:
    conn: sqlite3.Connection | None
    cursor: sqlite3.Cursor | None

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(PATH_DB)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY,
            name TEXT
        )
        ''')
        self.conn.commit()

    def insert(self, uid: int, name: str):
        self.cursor.execute(f"INSERT INTO user (id, name) VALUES ({uid}, '{name}')")
        self.conn.commit()

    def delete(self, uid: int):
        self.cursor.execute(f"DELETE FROM user WHERE id = {uid}")
        self.conn.commit()

    def query_by_uid(self, uid: int) -> str:
        return self.cursor.execute(f"SELECT * FROM user WHERE id = {uid}").fetchall()[0][1]

    def query_by_name(self, name: str) -> List[int]:
        results = self.cursor.execute(f"SELECT * FROM user WHERE name = '{name}'").fetchall()
        return [result[0] for result in results]

    def clear(self):
        self.cursor.execute("DROP TABLE user")
        self.conn.commit()

    def get_all(self) -> List[Tuple]:
        return self.cursor.execute("SELECT * FROM user").fetchall()

    def close(self):
        self.conn.close()
