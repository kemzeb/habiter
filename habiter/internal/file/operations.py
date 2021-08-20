"""This file provides the file operation logic for the files habiter
utilizes (e.g. using the context manager to reduce boilerplate project-wide)
"""

import pathlib
import sqlite3
from abc import ABC, abstractmethod


class AbstractFileOperations(ABC):
    """Abstract base class for file operations. 

    Instances of this class all share the __f_path static variable which can
    only be retrieved or set by the getter and setter class methods
    """
    __f_path: pathlib.Path = None

    @classmethod
    def get_f_path(cls) -> pathlib.Path:
        return cls.__f_path

    @classmethod
    def set_f_path(cls, f_path) -> None:
        cls.__f_path = f_path

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class SQLiteDataFileOperations(AbstractFileOperations):
    """Concrete class that provides database file operations using SQLite
    """

    def __init__(self):
        self.con = None
        self.cur = None

    def __enter__(self):
        self.con = sqlite3.connect(SQLiteDataFileOperations.get_f_path())
        # Allow having returned rows to map column names to values using
        # sqlite3.Row
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
        self.con.close()
