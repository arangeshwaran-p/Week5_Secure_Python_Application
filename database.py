"""SQLite persistence using parameterized SQL and explicit transactions."""
import sqlite3
from pathlib import Path

class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = str(Path(db_path))
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def create_user(self, username, salt, password_hash):
        try:
            with self.connection:
                self.connection.execute(
                    "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
                    (username, salt, password_hash)
                )
            return True
        except sqlite3.IntegrityError:
            raise RuntimeError("Username already exists.") from None

    def get_user(self, username):
        row = self.connection.execute(
            "SELECT username, salt, password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        return dict(row) if row else None

    def close(self):
        self.connection.close()
