import sqlite3

import telebot

from config import config, logger


def _connect():
    conn = sqlite3.connect(config.db_path, timeout=5.0)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    conn.execute('PRAGMA journal_mode = WAL')
    conn.execute('PRAGMA busy_timeout = 5000')

    return conn


def init_db():
    schema = """
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    with _connect() as conn:
        conn.executescript(schema)
        logger.info('Database initialized.')


def add_note(user_id: int, text: str) -> int:
    with _connect() as conn:
        cur = conn.execute(
            'INSERT INTO notes(user_id, text) VALUES (?, ?)',
            (user_id, text)
        )

        return cur.lastrowid


def list_notes(user_id: int, limit: int = 10, offset: int = 0) -> list:
    with _connect() as conn:
        cur = conn.execute(
            '''SELECT id, text, created_at
            FROM notes
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            OFFSET ?''',
            (user_id, limit, offset)
        )

        return cur.fetchall()


def find_note(user_id: int, text: str, limit: int = 10, offset: int = 0) -> list:
    with _connect() as conn:
        cur = conn.execute(
            '''SELECT id, text, created_at
            FROM notes
            WHERE user_id = ?
            AND text like '%' || ? || '%' COLLATE NOCASE
            ORDER BY id DESC
            LIMIT ?
            OFFSET ?''',
            (user_id, text, limit, offset)
        )

        return cur.fetchall()


def update_note(user_id: int, note_id: int, text: str) -> bool:
    with _connect() as conn:
        cur = conn.execute(
            '''UPDATE notes
            SET text = ?
            WHERE user_id = ?
            AND id = ?''',
            (text, user_id, note_id)
        )

        return cur.rowcount > 0


def delete_note(user_id: int, note_id: int) -> bool:
    with _connect() as conn:
        cur = conn.execute(
            '''DELETE FROM notes
            WHERE user_id = ?
            AND id = ?''',
            (user_id, note_id)
        )

        return cur.rowcount > 0


def count_notes(user_id: int, text = '') -> int:
    with _connect() as conn:
        cur = conn.execute(
            '''SELECT COUNT(*)
            FROM notes
            WHERE user_id = ?
            AND text like '%' || ? || '%' COLLATE NOCASE''',
            (user_id, text)
        )

        return cur.fetchone()[0]
