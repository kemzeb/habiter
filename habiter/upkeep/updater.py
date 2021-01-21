'''
'   updater.py
'
'   Handles updating the JSON file data and
'   also detects and will eventually be able to
'   update outdated versions of Habiter to maintain
'   compatibility
'''

import json
import sys
import datetime as date
import os

import habiter.math as habmath

from habiter.utils.messenger import (
    display_wrap_message, 
    display_error_message, 
    display_internal_error_message
)


HABITER_VERSION     = "1.0.2-rc.4"
HAB_DATE_FORMAT     = "%d, %b, %Y %H:%M%p"
HAB_JSON_IND        = 2


class HabiterUpdater:
    def __init__(self, filePath:str):
        self.fp = filePath
        self.date = date.datetime.now()

        self.create_record() # Ensures the record file can be communicated with
        self.update_habiter() # Updates habiter when needed


    def update_habiter(self):
        ''' updater_habiter() -> None
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
            version     last_logged
        '''

        try:
            with open(self.fp, 'r') as fh:
                data = json.load(fh)

            # Update current date and version 
            data["util"]["version"] = HABITER_VERSION

            loggedTime  = date.datetime.strptime( data["util"]["last_logged"], HAB_DATE_FORMAT ).date()
            presentTime = date.datetime.now().date()

            # Check if habit data has been updated
            if loggedTime >= presentTime:
                return
            # Else habit data has NOT been updated
            else:
                # Inform end user when habiter was last accessed AND update last logged to now
                print("\n[habiter] Last accessed: {}\n".format(data["util"]["last_logged"]))
                data["util"]["last_logged"] = self.date.strftime(HAB_DATE_FORMAT)
            
                # Compare present date to each last updated habit 
                for habit in data["habits"]:
                    # Has the habit been recently active
                    if habit["date_info"]["active"] is True:
                        habitDate = date.datetime.strptime( habit["date_info"]["last_updated"], HAB_DATE_FORMAT ).date()

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
            display_internal_error_message(f"JSON decoding error; Habit data file at \"{self.fp}\" may have been tampered with.")
            sys.exit(1)
        except KeyError:
            display_internal_error_message(f"There exists at least one key within the record that is no longer accessible.")
            sys.exit(1)
        
        else:
            # Write new data to .json file
            with open(self.fp, 'w') as fh:
                json.dump(data, fh, indent=HAB_JSON_IND)


    ##
    # Helper Methods
    ##


    def create_record(self):
        '''
            Creates a record if the specified file path either
            does NOT exist OR does exist and is empty
        '''
        if not os.path.isfile(self.fp) or os.stat(self.fp).st_size <= 0:
            # Initalize JSON arrays to hold JSON objects
            initFileContents = {
                        "util": {
                         "version": HABITER_VERSION,
                         "last_logged": date.datetime.now().strftime(HAB_DATE_FORMAT)
                        },
                        "habits": []
                        }

            with open(self.fp, 'w') as fh:
                json.dump(initFileContents, fh, indent=HAB_JSON_IND)


#---- Private helper methods; used for manipualting habit metadata organization
#-- Will be moved to different module that handles backwards compatibility
    def _add_key_into_list_dicts(self, listName:str, key:str, initVal=None):
        count = 0

        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        # Does the list exist
        if listName not in data:
            print(f"[internal_err: ADD_KEY]  The list \"{listName}\" does not exist within the record.")
            return

        # Add keys if they don't already exist
        for obj in data[listName]:
            if key not in obj:
                obj[key] = initVal
                count += 1
            else:
                print(f"[err: ADD_KEY]  Key with the name \"{key}\" already exists.")

        with open(self.fp, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)
        print(f"[habiter]  Added {count} \"{key}\" keys into the list \"{listName}\".")


    def _del_key_from_list_dicts(self, listName:str, key:str):
        count = 0

        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        # Does the list exist
        if listName not in data:
            print(f"[internal_err: DEL_KEY]  The list \"{listName}\" does not exist within the record.")
            return

        # Delete keys if they haven't already been deleted
        for obj in data[listName]:
            if key in obj:
                obj.pop(key)
                count += 1
            else:
                print(f"[err: DEL_KEY]  No key with the name \"{key}\".")

        # Write new data to .json file
        with open(self.fp, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)
        print(f"[habiter]  Deleted {count} \"{key}\" keys from the list \"{listName}\".")
