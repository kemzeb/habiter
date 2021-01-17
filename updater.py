'''
'   updater.py
'
'   Handles updating the JSON file data and
'   also detects and will eventually be able to
'   update outdated versions of Habiter to maintain
'   compatibility
'''

# NOTE: ensure standard datetime format

import json
import sys
import datetime as date
import os.path as path

import habiter_math as habmath

# Constants
HABITER_VERSION = "0.2.0"
HAB_DATE_FORMAT = "%d, %b, %Y %H:%M%p"
HAB_JSON_FPATH  = "records.json"
HAB_JSON_IND    = 2


class HabiterUpdater:
    def __init__(self, filePath):
        self.fp = filePath
        self.date = date.datetime.now()

        self.update_habiter()


    # Note that this method simply ignores inactivity of Habiter and updates where it left off
    def update_habiter(self):
        ''' Updates habit data based on user activity

        This method will update all the habit data if it detects
        that the date it was last logged has passed a certain
        wait period (i.e. if a day has passed). It updates just once
        and waits for habiter to be exectued once again that will meet
        the target condtion mentioned.

        Parameters (to be considered for implementation)

            waitPeriod:     quantity that represents the amount of time 
                            before Habiter updates habit data 
            unit:           unit of time (i.e. seconds, hours, days)
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
                print("\n[Habiter] Last accessed: {}\n".format(data["util"]["last_logged"]))
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
            print(f"[INTERNAL_ERR: UPDATE_HABITER: JSON decoding error; \"{HAB_JSON_FPATH}\" may have been tampered with.]")
            sys.exit(1)
        except KeyError:
            print(f"[INTERNAL_ERR: UPDATE_HABITER: There exists at least one key within the record that is no longer accessible.]")
            sys.exit(1)
        else:
            # Write new data to .json file
            with open(self.fp, 'w') as fh:
                json.dump(data, fh, indent=HAB_JSON_IND)


    # This method may be used in the future to aid in backwards compatibility
    def check_version(self):
        raise NotImplementedError


    ##
    # Helper Methods
    ##


    def add_key_into_list_dicts(self, listName:str, key:str, initVal=None):
        count = 0

        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        # Does the list exist
        if listName not in data:
            print(f"[ERROR: ADD_KEY FROM LIST: The list \"{listName}\" does not exist within the record.]")
            return

        # Add keys if they don't already exist
        for obj in data[listName]:
            if key not in obj:
                obj[key] = initVal
                count += 1
            else:
                print(f"[ERROR: ADD_KEY INTO LIST: Key with the name \"{key}\" already exists.]")

        with open(self.fp, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)
        print(f"[Added {count} \"{key}\" keys into the list \"{listName}\".]")


    def del_key_from_list_dicts(self, listName:str, key:str):
        count = 0

        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        # Does the list exist
        if listName not in data:
            print(f"[ERROR: DEL_KEY FROM LIST: The list \"{listName}\" does not exist within the record.]")
            return

        # Delete keys if they haven't already been deleted
        for obj in data[listName]:
            if key in obj:
                obj.pop(key)
                count += 1
            else:
                print(f"[ERROR: DEL_KEY FROM LIST: No key with the name \"{key}\".]")

        # Write new data to .json file
        with open(self.fp, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)
        print(f"[Deleted {count} \"{key}\" keys from the list \"{listName}\".]")
