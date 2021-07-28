"""
'   updater.py
'
'   Handles updating user habit data
"""

import datetime as date
import json
import sys
from abc import ABC, abstractmethod

import habiter.internal.math as habmath
from habiter import __version__
from habiter.internal.utils.consts import (
    HAB_TRACE_FPATH,
    HAB_DATE_FORMAT,
    HAB_JSON_IND
)
from habiter.internal.utils.messenger import (
    echo_internal_failure, echo_info
)


class AbstractFileUpdater(ABC):
    """Abstract class that provides file updating behaviors"""

    @abstractmethod
    def update(self, f_path: str) -> None:
        """Abstract method that updates the contents of a file"""
        pass


class JSONDataFileUpdater(AbstractFileUpdater):

    def update(self, f_path: str) -> None:
        """
        Updates habit data based on user activity

        This method will update all the habit data if it detects
        that the date it was last logged has passed a certain
        wait period (i.e. if a day has passed). It updates just once
        and waits for habiter to be executed once again that will meet
        this target condition.

        Note that it will update the following keys if needed:
            prev_occ    n_trials
            active      avg
            occ

        The following is always updated upon execution:
            last_logged
        """

        try:
            with open(HAB_TRACE_FPATH, 'r') as fh:
                data = json.load(fh)
        except json.JSONDecodeError:
            echo_internal_failure(
                f"JSON decoding error; Habit data file at \"{HAB_TRACE_FPATH}\" has failed to decode.")
            sys.exit(1)

        else:
            # Update current date and version
            data["util"]["version"] = __version__

            loggedTime = date.datetime.strptime(data["util"]["last_logged"],
                                                HAB_DATE_FORMAT).date()
            presentTime = date.datetime.now().date()

            # Check if habit data has been updated
            if loggedTime >= presentTime:
                return
            # Else habit data has NOT been updated
            else:
                echo_info("Last accessed: {}\n".format(data["util"]["last_logged"]))
                data["util"]["last_logged"] = date.datetime.now().strftime(HAB_DATE_FORMAT)

                # Compare present date to each last updated habit
                for habit in data["habits"]:
                    # Has the habit been recently active
                    if habit["date_info"]["active"] is True:
                        habitDate = date.datetime.strptime(habit["date_info"]["last_updated"], HAB_DATE_FORMAT).date()

                        # Has the date stored in this habit object already passed
                        if habitDate < presentTime:
                            # If so, that means we need to update its information
                            habit["prev_occ"] = None
                            habit["n_trials"] += 1
                            habit["date_info"]["active"] = False
                            habit["avg"] = habmath.avg(habit["total_occ"],
                                                       habit["n_trials"])
                            habit["occ"] = 0
                # Write new data to .json file
                with open(HAB_TRACE_FPATH, 'w') as fh:
                    json.dump(data, fh, indent=HAB_JSON_IND)
