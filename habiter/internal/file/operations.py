"""This file provides the file operation logic for the files habiter
utilizes (e.g. using the context manager to reduce boilerplate project-wide)
"""

import sqlite3
from abc import ABC, abstractmethod
from habiter.internal.utils.consts import HAB_DATE_FORMAT


class AbstractFileOperations(ABC):
    """Abstract base class for file operations
    """

    def __init__(self, f_path: str):
        self.f_path = f_path

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class SQLiteDataFileOperations(AbstractFileOperations):
    """Concrete class that provides database file operations with SQLite
    """

    def __init__(self, f_path: str):
        super().__init__(f_path)
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
