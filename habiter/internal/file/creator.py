"""
This file contains implementations involving
the creation of files used to r/w data
"""

import os
import json
import sqlite3
from datetime import datetime

from abc import ABC, abstractmethod

from habiter import __version__

from habiter.internal.utils.consts import HAB_DATE_FORMAT, HAB_JSON_IND
from habiter.internal.file.operations import SQLiteDataFileOperations


class AbstractFileCreator(ABC):
    """An abstract class that defines file creation behaviors"""

    def create(self, dir_path: str, f_name: str) -> None:
        """Creates a file with a directory path that is also recursively created if needed

        Parameters
        ----------
        dir_path: str
            The directory path in which the created file will reside
        f_name: str
            The name of the file to be created
        """
        # Does the path exist
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        data_file_path = os.path.join(dir_path, f_name)
        if not os.path.isfile(data_file_path):
            self._init_file(data_file_path)

    @abstractmethod
    def _init_file(self, f_path: str) -> None:
        """Abstract method that creates and initializes the contents of a file

        Parameters
        ----------
        f_path: str
            File path to the file that is to be created
        """
        pass


class SQLiteDataFileCreator(AbstractFileCreator):
    def _init_file(self, f_path: str) -> None:

        with SQLiteDataFileOperations(f_path) as fop:
            # Create META_INFO table
            fop.cur.execute('''
            CREATE TABLE meta_info
            (meta_id        INTEGER  PRIMARY KEY AUTOINCREMENT,          
                version        TEXT             NOT NULL,
                last_logged    TEXT             NOT NULL
            )
            ''')
            # Create HABIT table
            fop.cur.execute('''
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
            fop.cur.execute('INSERT INTO meta_info(version, last_logged) '
                            'VALUES (?, ?)',
                            (__version__,
                             datetime.now().strftime(HAB_DATE_FORMAT)))


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
