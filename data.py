import sqlite3, os

DB_FILE = "stegano_users.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            app_password_set INTEGER DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS key_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            key_used TEXT,
            file_name TEXT,
            recipient TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def log_key(email, key, filename, recipient):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO key_logs (email, key_used, file_name, recipient)
        VALUES (?, ?, ?, ?)
    """, (email, key, filename, recipient))
    conn.commit()
    conn.close()
