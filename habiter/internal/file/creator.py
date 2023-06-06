"""
This file contains implementations involving
the creation of files used to r/w data
"""

import pathlib
import sqlite3
from datetime import datetime
from abc import ABC, abstractmethod

from habiter import __version__
from habiter.internal.utils.consts import DB_DATE_FORMAT


class AbstractFileCreator(ABC):
    """An abstract class that defines file creation behaviors."""

    def __init__(self, dir_path: str, name: str):
        self.dir_path = pathlib.Path(dir_path)
        self.name = name
        self.data_file_path = self.dir_path / self.name

    def get_data_file_path(self) -> pathlib.Path:
        return self.data_file_path

    def create(self) -> None:
        """Creates a file with a directory path that is also recursively created if
        needed."""
        if not self.dir_path.exists():
            self.dir_path.mkdir(parents=True)

        if not self.data_file_path.exists():
            self._initialize()

    @abstractmethod
    def _initialize(self) -> None:
        """Abstract method that creates and initializes the contents of a file."""
        pass


class SQLiteDataFileCreator(AbstractFileCreator):
    def _initialize(self) -> None:
        con = sqlite3.connect(self.data_file_path)

        # Create META_INFO table.
        con.execute(
            """
        CREATE TABLE meta_info
        (meta_id        INTEGER  PRIMARY KEY AUTOINCREMENT,
            version        TEXT             NOT NULL,
            last_logged    TEXT             NOT NULL
        )
        """
        )
        # Create HABIT table.
        con.execute(
            """
                CREATE TABLE habit
                (
                    habit_id       INTEGER  PRIMARY KEY AUTOINCREMENT,
                    habit_name     TEXT              NOT NULL,
                    curr_tally     INT               NOT NULL,
                    total_tally    INT               NOT NULL,
                    num_of_trials  INT               NOT NULL,
                    wait_period    INT               NULL,
                    is_active      BOOLEAN           NOT NULL,
                    last_updated   TEXT              NOT NULL,
                    date_added     TEXT              NOT NULL,
                    prev_tally     INT               NULL
                )
                """
        )
        # Initialize META_INFO table.
        con.execute(
            "INSERT INTO meta_info(version, last_logged) " "VALUES (?, ?)",
            (__version__, datetime.now().strftime(DB_DATE_FORMAT)),
        )
        con.commit()
        con.close()
