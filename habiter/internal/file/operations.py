import sqlite3
import datetime
from habiter.internal.utils.consts import HAB_DATE_FORMAT


class SQLiteDataFileOperations:
    """Concrete class that defines database file operations with SQLite

    This class is mainly used throughout the codebase that requires access
    to the database file as a context manager to reduce boilerplate
    """

    def __init__(self, f_path: str):
        self.f_path = f_path
        self.con = None
        self.cur = None

    def __enter__(self):
        self.con = sqlite3.connect(self.f_path)
        # Allow having returned rows to map column names to values using
        # sqlite3.Row
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
        self.con.close()
