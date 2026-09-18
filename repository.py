"""
repository.py

Owns all database access for the Library Management System.
No UI code lives here, and no other module runs SQL directly —
every read/write to the Library table goes through this class.
This is the Repository pattern: it separates data-access logic
from business logic and UI logic, so each can change independently
and the data layer can be unit-tested without a GUI.
"""

import sqlite3


class LibraryRepository:
    def __init__(self, db_path="library.db"):
        self.connector = sqlite3.connect(db_path)
        self.cursor = self.connector.cursor()
        self._create_table()

    def _create_table(self):
        self.connector.execute(
            """CREATE TABLE IF NOT EXISTS Library (
                BK_NAME TEXT,
                BK_ID TEXT PRIMARY KEY NOT NULL,
                AUTHOR_NAME TEXT,
                BK_STATUS TEXT,
                CARD_ID TEXT
            )"""
        )
        self.connector.commit()

    def add_book(self, bk_name, bk_id, author_name, bk_status, card_id):
        """Raises sqlite3.IntegrityError if bk_id already exists."""
        self.connector.execute(
            "INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID) "
            "VALUES (?, ?, ?, ?, ?)",
            (bk_name, bk_id, author_name, bk_status, card_id),
        )
        self.connector.commit()

    def get_all_books(self):
        cursor = self.connector.execute("SELECT * FROM Library")
        return cursor.fetchall()

    def get_book(self, bk_id):
        cursor = self.connector.execute(
            "SELECT * FROM Library WHERE BK_ID=?", (bk_id,)
        )
        return cursor.fetchone()

    def update_book(self, bk_id, bk_name, bk_status, author_name, card_id):
        self.cursor.execute(
            "UPDATE Library SET BK_NAME=?, BK_STATUS=?, AUTHOR_NAME=?, CARD_ID=? "
            "WHERE BK_ID=?",
            (bk_name, bk_status, author_name, card_id, bk_id),
        )
        self.connector.commit()

    def update_status(self, bk_id, bk_status, card_id):
        self.cursor.execute(
            "UPDATE Library SET BK_STATUS=?, CARD_ID=? WHERE BK_ID=?",
            (bk_status, card_id, bk_id),
        )
        self.connector.commit()

    def delete_book(self, bk_id):
        self.cursor.execute("DELETE FROM Library WHERE BK_ID=?", (bk_id,))
        self.connector.commit()

    def delete_all_books(self):
        self.cursor.execute("DELETE FROM Library")
        self.connector.commit()

    def close(self):
        self.connector.close()
