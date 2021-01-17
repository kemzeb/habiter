'''JSON module 
'
' Provides essential .json file R/W and manipulation behaviors
' as well as the shell display of its results
'''

# In the future I may need to create variables for CLI attributes
# just in case they're renamed

import json
import datetime as date
import os
import sys

import habiter_math as habmath

from updater import HAB_DATE_FORMAT, HAB_JSON_FPATH, HAB_JSON_IND, HABITER_VERSION
from updater import HabiterUpdater


class Habiter:
    def __init__(self, filePath:str):
        self.fp = filePath

        # Create a JSON record IFF it does not exist OR contents are empty
        self.create_record()

        # Update record each time habiter is executed
        ## This method also handles incompatibile JSON
        # exceptions 
        HabiterUpdater(HAB_JSON_FPATH)


    def occurrence(self, args, numOfOcc = 1):
        # Cast to set to remove possible duplicates
        args = set(args)

        # Read up-to-date record
        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        for arg in args:
            index = self.search_record_for_habit(arg, data) # search for index matching current habit name

            if index != None:
                # Check it the '--zero' flag has been used and has there already been occ's captured
                if numOfOcc == 0 and data["habits"][index]["occ"] > 0:
                    print(f"[ERROR: OCC: Habit \"{arg}\" contains occurrences.]")
                    continue

                # Update habit data
                habit = data["habits"][index] 
                habit["prev_occ"]   = data["habits"][index]["occ"] # Capture previous occurrence
                habit["occ"]        += numOfOcc
                habit["total_occ"]   += numOfOcc

                # Update date information
                habit["date_info"]["last_updated"]  = f"{date.datetime.now().strftime(HAB_DATE_FORMAT)}"
                habit["date_info"]["active"]        = True

                data["habits"][index] = habit
            
                print("[Habit \"{}\" occurrence updated from {} to {}.]".format(arg, 
                                                                        habit["prev_occ"], 
                                                                        habit["occ"]))
            else:
                print(f"[ERROR: OCC: Habit \"{arg}\" does not exist.]")

        # Write new data to .json file    
        with open(self.fp, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)


    def add_habits(self, *args):
        # Cast to set to remove possible duplicates
        args = set(args)

        # Read up-to-date record
        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        for arg in args:
            # Search habit data for duplicates
            index = self.search_record_for_habit(arg, data)

            if index is None:
                newHabitObj = self.init_habit(arg)
                data["habits"].append(newHabitObj) 
                print(f"[Habit \"{arg}\" has been added.]")
            else:
                print(f"[ERROR: ADD: Habit \"{arg}\" already exists.]")

        # Write new data to .json file
        with open(self.fp, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)


    def delete_habits(self, *args):
        if self.inquire_choice("make a deletion") is False:
            sys.exit(0)
   
        # Read up-to-date record
        with open(self.fp, 'r') as fh:
            data = json.load(fh)

            if len(data["habits"]) <= 0:
                print("[ERROR: DEL: Cannot delete from an empty habit list.]")
            else:
                for arg in args:
                    index = self.search_record_for_habit(arg, data)

                    if index != None:
                        data["habits"].pop(index) # Remove dict from "habits" list
                        print(f"[Habit \"{arg}\" has been deleted.]")
                    else:
                        print(f"[ERROR: DEL: No habit with the name \"{arg}\".]")

        # Write new data to .json file
        with open(self.fp, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)


    def reset_habits(self, *args):
        # Confirm end user choice
        if self.inquire_choice("reset some habit(s)") is False:
            sys.exit(0)

        # Read up-to-date record
        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        for arg in args:
            index = self.search_record_for_habit(arg, data)
            
            if index != None:
                # Capture date added before using 'init_habit()'
                ## Until I can find a better improvement, this
                #  is how we avoid replacing date added with 
                #  a new date
                dateAdded = data["habits"][index]["date_info"]["date_added"]
                data["habits"][index] = self.init_habit(arg, dateAdded)

                print(f"[Habit \"{arg}\" has been reset.]")
            else:
                print(f"[ERROR: RESET: No habit with the name \"{arg}\".]")

        with open(self.fp, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)
    

    def list_habits(self):
        # Read up-to-date record
        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        print("Habit\n-------------------")
        for habit in data["habits"]:
            print(habit["habit_name"])
        print("-------------------")

        
    def list_habits_k(self):
        # Read up-to-date record
        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        print("Habit + Attributes\t\t\tValue")
        print("-------------------\t\t\t-----")

        currDay =  date.datetime.strptime(data["util"]["last_logged"], HAB_DATE_FORMAT).date()

        for habit in data["habits"]:
            deltaDay = None
            if habit["date_info"]["last_updated"] != None:
                habitDay = date.datetime.strptime(habit["date_info"]["last_updated"], HAB_DATE_FORMAT).date()
                deltaDay = (currDay - habitDay).days # subtraction returns a timedelta

            print("[{}]".format( habit["habit_name"]) )
            prob = ((1 - 
                        habmath.poisson_prob(habit["avg"], 0) -      # Prob. occurring never
                        habmath.poisson_prob(habit["avg"], 1)) * 100) # Prob. occuring once
            probInfo = f"{prob:.3f}%" if habit["n_trials"] > 1 else "(More data required)"
            # For now the Poisson approx. display remains here
            print(f"  | P(Occurrences >= 2 today):\t\t{probInfo}")

            print("  | Today's occurrences:\t\t{}".format( habit["occ"]) )
            print("  | Total occurrences:\t\t\t{}".format( habit["total_occ"]) )
            print("  | # of days captured:\t\t\t{}".format( habit["n_trials"]) )
            print(f"  | Last updated:\t\t\t{deltaDay} day(s) ago")
            print("  | Date added:\t\t\t\t{}\n".format( habit["date_info"]["date_added"]) )
        print("-------------------\t\t\t-----")
        print("[Habiter] Disclaimer: More data captured = increased statistical accurracy!\n")

    
    # NOT YET IMPLEMENTED, DON'T USE 
    def list_habits_ks(self):
        # Read up-to-date record
        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        print("Habit\n-------------------")
        for habit in data["habits"]:
            prob = ((1 - 
                        habmath.poisson_prob(habit["avg"], 0) -      # Prob. occurring never
                        habmath.poisson_prob(habit["avg"], 1)) * 100) # Prob. occuring once
            print(habit["habit_name"])
            print(f"  | P(X >= 2) = {probability:.3f}%")
        print("-------------------")
        

    ######################################################################
    ##     Helper Methods
    ######################################################################


    # Returns an index of the first found dict, else None
    def search_record_for_habit(self, key, data):
        return next( (i for i, habit in enumerate(data["habits"]) if habit["habit_name"] == key), None)


    def inquire_choice(self, choice:str):
        print(f"\n[Habiter] Are you sure you want to {choice}? This cannot be undone.\n")
        ans = ''
        while True:
            ans = input("[Provide a y/n.]: ")

            if ans != "y" and ans != "n":
                print("[ERROR: INQUIRE_CHOICE: Answer provided incorrect; please try again.]")
            else:
                return True if ans == 'y' else False


    def create_record(self):
        '''
            Creates a record if the specified file path either
            does NOT exist OR does exist and is empty

            "updater.py" module investigates whether or not
            the file is compatible with the json module's decoder
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
                json.dump(initFileContents, fh, indent=HAB_JSON_IND)   # Convert to JSON and store into .json file


    # Note: "active" key represents if the habit saw new occurrences,
    # not if the habit data has been modified
    def init_habit(self, 
                    habitName: str, 
                    dateAdded = date.datetime.now().strftime(HAB_DATE_FORMAT)):
        ''' Initalizes a dict to be stored in the habit data
        
        Parameters
            habitName:  name of the habit to be added
            date:       date that it was added
        '''
        return {
            "habit_name": habitName,
            "occ": 0, 
            "total_occ": 0, 
            "prev_occ": None,
            "n_trials": 0,
            "avg": 0.0,
            "date_info":
            {
                "date_added": dateAdded,
                "last_updated": None,
                "active": False 
            }
            } 
