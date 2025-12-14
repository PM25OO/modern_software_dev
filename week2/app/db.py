from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Generator, Optional, List

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"


def ensure_data_directory_exists() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    ensure_data_directory_exists()
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    ensure_data_directory_exists()
    conn = get_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now'))
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS action_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note_id INTEGER,
                    text TEXT NOT NULL,
                    done INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (note_id) REFERENCES notes(id)
                );
                """
            )
    finally:
        conn.close()


def insert_note(conn: sqlite3.Connection, content: str) -> int:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    return int(cursor.lastrowid)


def list_notes(conn: sqlite3.Connection) -> List[sqlite3.Row]:
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
    return list(cursor.fetchall())


def get_note(conn: sqlite3.Connection, note_id: int) -> Optional[sqlite3.Row]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, content, created_at FROM notes WHERE id = ?",
        (note_id,),
    )
    row = cursor.fetchone()
    return row


def insert_action_items(conn: sqlite3.Connection, items: List[str], note_id: Optional[int] = None) -> List[int]:
    cursor = conn.cursor()
    ids: List[int] = []
    for item in items:
        cursor.execute(
            "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
            (note_id, item),
        )
        ids.append(int(cursor.lastrowid))
    conn.commit()
    return ids


def list_action_items(conn: sqlite3.Connection, note_id: Optional[int] = None) -> List[sqlite3.Row]:
    cursor = conn.cursor()
    if note_id is None:
        cursor.execute(
            "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC"
        )
    else:
        cursor.execute(
            "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
            (note_id,),
        )
    return list(cursor.fetchall())


def mark_action_item_done(conn: sqlite3.Connection, action_item_id: int, done: bool) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE action_items SET done = ? WHERE id = ?",
        (1 if done else 0, action_item_id),
    )
    conn.commit()


