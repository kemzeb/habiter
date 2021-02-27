'''
'   updater.py
'
'   Handles updating user habit data
'''

import json
import sys
import datetime as date
import os

import habiter.math as habmath

from habiter.utils.messenger import (
    display_message,
    display_error_message,
    display_internal_error_message
)
from habiter.utils.constants import (
    HAB_AUTHOR,     #..here to will handle Windows file structure... yuck
    HAB_DIR_FPATH,
    HAB_TRACE_FPATH,
    HAB_FDATA,
    HABITER_VERSION,
    HAB_DEFAULT_FPATH,
    HAB_DATE_FORMAT,
    HAB_JSON_IND
)


class HabiterUpdater:
    def __init__(self):
        self.date = date.datetime.now()

        self.create_record() # Ensures user habit data to communicate with
        self.update_habiter() # Updates habiter when needed


    def update_habiter(self):
        '''
        Updates habit data based on user activity

        This method will update all the habit data if it detects
        that the date it was last logged has passed a certain
        wait period (i.e. if a day has passed). It updates just once
        and waits for habiter to be exectued once again that will meet
        this target condtion.

        Note that it will update the following keys if needed:
            prev_occ    n_trials
            active      avg
            occ

        The following is always updated upon execution:
            last_logged
        '''

        try:
            with open(HAB_TRACE_FPATH, 'r') as fh:
                data = json.load(fh)

            # Update current date and version
            data["util"]["version"] = HABITER_VERSION

            loggedTime  = date.datetime.strptime( data["util"]["last_logged"],
                                HAB_DATE_FORMAT ).date()
            presentTime = date.datetime.now().date()

            # Check if habit data has been updated
            if loggedTime >= presentTime:
                return
            # Else habit data has NOT been updated
            else:
                # Inform end user when habiter was last accessed AND update last logged to now
                display_message("Last accessed: {}\n".format(data["util"]["last_logged"]))
                data["util"]["last_logged"] = self.date.strftime(HAB_DATE_FORMAT)

                # Compare present date to each last updated habit
                for habit in data["habits"]:
                    # Has the habit been recently active
                    if habit["date_info"]["active"] is True:
                        habitDate = date.datetime.strptime( \
                        habit["date_info"]["last_updated"], HAB_DATE_FORMAT ).date()

                        # Has the date stored in this habit object already passed
                        if habitDate < presentTime:
                            # If so, that means we need to update its information
                            habit["prev_occ"]           = None
                            habit["n_trials"]           += 1
                            habit["date_info"]["active"] = False
                            habit["avg"] = habmath.avg( habit["total_occ"],
                                                        habit["n_trials"])
                            habit["occ"] = 0
        except json.JSONDecodeError:
            display_internal_error_message(f"JSON decoding error; Habit data file at \"{HAB_TRACE_FPATH}\" may have been tampered with.")
            sys.exit(1)
        except KeyError:
            display_internal_error_message(f"There exists at least one key within the habit data that is no longer accessible.")
            sys.exit(1)

        else:
            # Write new data to .json file
            with open(HAB_TRACE_FPATH, 'w') as fh:
                json.dump(data, fh, indent=HAB_JSON_IND)


    def create_record(self):
        '''
            Creates a user habit data file path; creates a path to an OS's user
            data directory using the 'appdirs' module to find it in the first
            place.
        '''
        # Determine if user data directory exists
        if not os.path.isdir(HAB_DIR_FPATH):
            if sys.platform == 'win32':
                # Join OS user data path with HAB_AUTHOR directory
                os.mkdir(os.path.join(HAB_DEFAULT_FPATH, HAB_AUTHOR))
            # Add 'habiter' directory to path
            os.mkdir(HAB_DIR_FPATH)

        # Determine if user data file exists
        if not os.path.isfile(HAB_TRACE_FPATH):
            #.. if not, create it
            with open(HAB_TRACE_FPATH, 'w') as fh:
            # Initalize JSON arrays to hold JSON objects
                initFileContents = {
                            "util": {
                             "version": HABITER_VERSION,
                             "last_logged": date.datetime.now().strftime(HAB_DATE_FORMAT)
                            },
                            "habits": []
                            }

            with open(HAB_TRACE_FPATH, 'w') as fh:
                json.dump(initFileContents, fh, indent=HAB_JSON_IND)
