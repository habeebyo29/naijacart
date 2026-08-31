import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATABASE = BASE_DIR / "naijacart.db"


def get_db():
    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection