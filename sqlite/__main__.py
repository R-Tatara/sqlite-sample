#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sqlite3


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)5s : %(message)s',
)

class UserDatabase:
    def __init__(self, db_name="data/users.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def add_user(self, user_id: str, name: str, email: str) -> None:
        try:
            self.cursor.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)", (user_id, name, email))
            self.connection.commit()
            logging.info(f"User '{name}' added successfully.")
        except sqlite3.IntegrityError:
            logging.error(f"User with id '{user_id}' already exists.")

    def get_all_users(self) -> list[tuple]:
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def get_user_by_name(self, name: str) -> tuple | None:
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        return self.cursor.fetchone()

    def delete_user_by_name(self, name: str) -> None:
        self.cursor.execute("DELETE FROM users WHERE name = ?", (name,))
        self.connection.commit()
        logging.info(f"User '{name}' deleted successfully.")

    def close(self) -> None:
        self.connection.close()


def main():
    db = UserDatabase()

    # Add users
    db.add_user("1", "Alice", "alice@example.com")
    db.add_user("2", "Bob", "bob@example.com")

    # Get a specific user
    logging.info(f"User 'Alice': {db.get_user_by_name('Alice')}")

    # Get all users
    logging.info(f"All users: {db.get_all_users()}")

    # Delete a user
    db.delete_user_by_name("Bob")


if __name__ == "__main__":
    db = UserDatabase()
    try:
        main()
    finally:
        db.close()
