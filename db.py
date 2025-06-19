import sqlite3
from pathlib import Path

DB_PATH = Path("app.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


with get_conn() as conn:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            birthdate TEXT,
            current_grade INTEGER,
            class_year1 TEXT,
            class_year2 TEXT,
            class_year3 TEXT
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS invitations (
            token TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used INTEGER DEFAULT 0
        );
        """
    )

