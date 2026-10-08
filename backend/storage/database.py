import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "secure_cloud.db")


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS encrypted_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            encrypted_data TEXT NOT NULL,
            nonce TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def store_encrypted_data(encrypted_data, nonce):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO encrypted_data (encrypted_data, nonce)
        VALUES (?, ?)
    """, (encrypted_data, nonce))

    connection.commit()

    record_id = cursor.lastrowid

    connection.close()

    return record_id


def get_encrypted_data(record_id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, encrypted_data, nonce, created_at
        FROM encrypted_data
        WHERE id = ?
    """, (record_id,))

    record = cursor.fetchone()

    connection.close()

    if record:
        return dict(record)

    return None