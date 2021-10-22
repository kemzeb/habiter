"""
This file contains implementations involving
the creation of files used to r/w data
"""

import pathlib
import os
import json
import sqlite3
from datetime import datetime
from abc import ABC, abstractmethod

from habiter import __version__
from habiter.internal.utils.consts import HAB_DATE_FORMAT, HAB_JSON_IND


class AbstractFileCreator(ABC):
    """An abstract class that defines file creation behaviors"""

    def __init__(self, dir_path: str, f_name: str):
        self.dir_path = pathlib.Path(dir_path)
        self.f_name = f_name
        self.data_f_path = self.dir_path / self.f_name

    def get_data_f_path(self) -> pathlib.Path:
        return self.data_f_path

    def create(self) -> None:
        """Creates a file with a directory path that is also recursively created if needed
        """
        # Does the child directory exist
        if not self.dir_path.exists():
            self.dir_path.mkdir(parents=True)

        if not self.data_f_path.exists():
            self._init_file()

    @abstractmethod
    def _init_file(self) -> None:
        """Abstract method that creates and initializes the contents of a file
        """
        pass


class SQLiteDataFileCreator(AbstractFileCreator):
    def _init_file(self) -> None:
        con = sqlite3.connect(self.data_f_path)

        # Create META_INFO table
        con.execute('''
        CREATE TABLE meta_info
        (meta_id        INTEGER  PRIMARY KEY AUTOINCREMENT,          
            version        TEXT             NOT NULL,
            last_logged    TEXT             NOT NULL
        )
        ''')
        # Create HABIT table
        con.execute('''
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
                ''')
        # Initialize META_INFO table
        con.execute('INSERT INTO meta_info(version, last_logged) '
                    'VALUES (?, ?)',
                    (__version__,
                     datetime.now().strftime(HAB_DATE_FORMAT)))
        con.commit()
        con.close()


class JSONDataFileCreator(AbstractFileCreator):
    """Concrete class that held the original creation logic for the habiter data file.

    This will most likely be removed in future iterations but will be kept
    in case configuration files are introduced and the logic can be utilized
    in a similar manner.
    """

    def _init_file(self, f_path: str) -> None:
        with open(f_path, 'w') as f:
            # Initialize JSON arrays to hold JSON objects
            initFileContents = {
                "util": {
                    "version": __version__,
                    "last_logged": datetime.now().strftime(HAB_DATE_FORMAT)
                },
                "habits": []
            }
            json.dump(initFileContents, f, indent=HAB_JSON_IND)
