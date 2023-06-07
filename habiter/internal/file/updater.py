"""
'   updater.py
'
'   Handles updating user habit data
"""


import pathlib
from abc import ABC, abstractmethod
from datetime import datetime

from habiter import __version__
from habiter.internal.file.operations import SQLiteDataFileOperations
from habiter.internal.utils.consts import DB_DATE_FORMAT
from habiter.internal.utils.messenger import echo_info


class AbstractFileUpdater(ABC):
    """Abstract class that provides file updating behaviors"""

    def __init__(self, f_path: pathlib.Path) -> None:
        self.f_path = f_path

    @abstractmethod
    def update(self) -> None:
        """Abstract method that updates the contents of a file"""
        pass


class SQLiteDataFileUpdater(AbstractFileUpdater):
    def update(self) -> None:
        with SQLiteDataFileOperations() as fo:
            fo.cur.execute("SELECT * FROM meta_info")
            # There should be a single row from the meta_info table
            row = fo.cur.fetchone()

            logged_time = datetime.strptime(row["last_logged"], DB_DATE_FORMAT).date()
            curr_time = datetime.now().date()

            # Check if habit data has already been updated
            if logged_time >= curr_time:
                return

            echo_info("Last accessed: {}\n".format(row["last_logged"]))

            # Update row
            fo.cur.execute(
                "UPDATE meta_info SET version=?, " "last_logged=? WHERE meta_id=?",
                (__version__, datetime.now().strftime(DB_DATE_FORMAT), row["meta_id"]),
            )
            # Retrieve all habit data with active column set to 'True'
            fo.cur.execute(
                "SELECT curr_tally, prev_tally, is_active, "
                "last_updated, num_of_trials, habit_name, habit_id "
                "FROM habit WHERE is_active=True"
            )
            data = fo.cur.fetchall()
            for habit in data:
                habit_date = datetime.strptime(
                    habit["last_updated"], DB_DATE_FORMAT
                ).date()
                if habit_date < curr_time:
                    prev_tally = 0
                    num_of_trials = habit["num_of_trials"] + 1
                    is_active = False
                    curr_tally = 0
                    fo.cur.execute(
                        "UPDATE habit SET "
                        "prev_tally = ?, num_of_trials = ?, "
                        "is_active = ?, curr_tally = ? "
                        "WHERE habit_id = ?",
                        (
                            prev_tally,
                            num_of_trials,
                            is_active,
                            curr_tally,
                            habit["habit_id"],
                        ),
                    )
