'''
' Provides essential .json file R/W and manipulation behaviors
' as well as the shell display of its results
'''

# In the future I may need to create variables for CLI attributes
# just in case they're renamed

import json
import datetime as date
import os
import sys

import habiter.math as habmath

from habiter.utils.messenger import display_message, display_error_message, display_wrap_message
from habiter.data import HAB_TRACE_FPATH

from habiter.upkeep.updater import (
    # Constants
    HAB_DATE_FORMAT,  
    HAB_JSON_IND, 
    HABITER_VERSION,
    
    # Classes
    HabiterUpdater 
) 


def ensure_record_exists(recordName:str):
        ''' ensure_record_exists() -> string
            
            Checks 'trace.txt' if it contains a absPath. If
            it does not exist, prompt user for an absolute
            file path. It returns a string file path.

            This is done to allow habit data to not be overwritten
            by new habiter versions. 

            Though I am not a big fan with how I handled 
            having the habit data on a local machine, using pip makes 
            it bit a tad complicated to the point where I see this as 
            the best way to have data that cannot be overwritten when 
            pip installs new habiter versions on user's local machines.
        '''
        try:
            # Check 'trace.txt' if a path to habit data already exists
            with open(HAB_TRACE_FPATH, 'r') as f:
                absPath = f.readline()
        except OSError as err:
            display_error_message(f"OS Error: {err}")
            sys.exit(1)

        # Check if path + habit data file stored within file does not exist
        if not os.path.exists(absPath) or absPath == '':

            ## Displaying messages is in a messy state 
            #  as of now, it needs to be updated
            message = f'''habiter v{HABITER_VERSION} does not detect a file path to hold habit data. \
            Please provide an absolute path that ends with a directory that will \
            hold your data.'''
            display_wrap_message(message)
            print()

            message = '''\tNote, please don't provide a path that relates to habiter's location! It will be deleted when you upgrade to a different version. Due to this nature, you will also need to provide a file path each time you upgrade!'''
            display_wrap_message(message, False)
            try:
                absPath = input("  [Provide an absolute path]: ")   # Gather input
                viablePath = os.path.join(absPath, recordName)      # Create path to record data
            except KeyboardInterrupt:
                sys.exit(0)

            # Ensure given file path exists 
            if not os.path.exists(absPath):
                display_error_message(f"Invalid absolute path.")
                sys.exit(1)

            # Attempt to create record at given absolute path 
            try:
                f = open(viablePath, 'w')
            except OSError as err:
                display_error_message(f"OS Error: {err}")
                sys.exit(1)
            finally:
                if f:
                    f.close()

            # Attempt to store viable path for future use 
            try:
                with open(HAB_TRACE_FPATH, 'w') as f:
                    f.write(viablePath)
            except OSError as err:
                display_error_message(f"OS Error: {err}")
                sys.exit(1)
            else:
                return viablePath

        # Path and habit data must already exist
        else:
            return absPath


class Habiter:
    def __init__(self):
        self.fp = ensure_record_exists("records.json")

        # Update record each time habiter is executed
        ## This method also handles incompatibile JSON
        # exceptions 
        HabiterUpdater(self.fp)


    def tally_habits(self, args, numOfOcc = 1):
        # Cast to set to remove possible duplicates
        args = set(args)

        # Read up-to-date record
        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        for arg in args:
            index = self.search_record_for_habit(arg, data) # search for index matching current habit name

            if index != None:
                # Check it the '--zero' flag has been used and has there already been tallies captured
                if numOfOcc == 0 and data["habits"][index]["occ"] > 0:
                    display_error_message(f"Habit \"{arg}\" contains occurrences.")
                    continue

                # Update habit data
                habit = data["habits"][index] 
                habit["prev_occ"]   = habit["occ"] # Capture previous tally
                habit["occ"]        += numOfOcc
                habit["total_occ"]  += numOfOcc

                # Update date information
                habit["date_info"]["last_updated"]  = f"{date.datetime.now().strftime(HAB_DATE_FORMAT)}"
                habit["date_info"]["active"]        = True

                data["habits"][index] = habit
            
                display_message("Habit \"{}\" tally updated from {} to {}.".format(arg, 
                                                                        habit["prev_occ"], 
                                                                        habit["occ"]))
            else:
                display_error_message(f"Habit \"{arg}\" does not exist.")

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
                display_message(f"Habit \"{arg}\" has been added.")
            else:
                display_error_message(f"Habit \"{arg}\" already exists.")

        # Write new data to .json file
        with open(self.fp, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)


    def delete_habits(self, *args):
        # Cast to set to remove possible duplicates
        args = set(args)

        # Confirm end user choice
        if self.inquire_choice("make a deletion") is False:
            sys.exit(0)
   
        # Read up-to-date record
        with open(self.fp, 'r') as fh:
            data = json.load(fh)

            if len(data["habits"]) <= 0:
                display_error_message("Cannot delete from an empty habit list.")
            else:
                for arg in args:
                    index = self.search_record_for_habit(arg, data)

                    if index != None:
                        data["habits"].pop(index) # Remove dict from "habits" list
                        display_message(f"Habit \"{arg}\" has been deleted.")
                    else:
                        display_error_message(f"No habit with the name \"{arg}\".")

        # Write new data to .json file
        with open(self.fp, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)


    def reset_habits(self, *args):
        # Cast to set to remove possible duplicates
        args = set(args)

        # Confirm end user choice
        if self.inquire_choice("reset some habit(s)") is False:
            sys.exit(0)

        # Read up-to-date record
        with open(self.fp, 'r') as fh:
            data = json.load(fh)

        for arg in args:
            index = self.search_record_for_habit(arg, data)
            
            if index != None:
                dateAdded = data["habits"][index]["date_info"]["date_added"]
                data["habits"][index] = self.init_habit(arg, dateAdded)

                display_message(f"Habit \"{arg}\" has been reset.")
            else:
                display_error_message(f"No habit with the name \"{arg}\".")

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

            print("  | Today's daily tally:\t\t{}".format( habit["occ"]) )
            print("  | Total tally:\t\t\t{}".format( habit["total_occ"]) )
            print("  | # of days captured:\t\t\t{}".format( habit["n_trials"]) )
            print(f"  | Last updated:\t\t\t{deltaDay} day(s) ago")
            print("  | Date added:\t\t\t\t{}\n".format( habit["date_info"]["date_added"]) )
        print("-------------------\t\t\t-----")
        display_message("Note: More data captured = increased statistical accurracy!\n")


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

#---Main Options-----------------------------

    def set_record(self, recordName:str):
        ''' set_record() -> None

        Sets a new file path for habit data to be 
        stored. It also deletes the previous record
        if it was specified in 'trace.txt'

        Analogous to 'ensure_record_exists()'
        '''

        message = '''\tNote, please don't provide a path that relates to habiter's location! It will be deleted when you upgrade to a different version. Due to this nature, you will also need to provide a file path each time you upgrade!'''
        display_wrap_message(message, False)

        # Gather user input. Afterwards we append the record file to the end
        # of the path. 
        userPath = input("  [Provide an absolute path]: ")   
        viablePath = os.path.join(userPath, recordName) 
        print(f"viable {viablePath}")
        # Ensure user file path exists 
        if not os.path.exists(userPath):
            display_error_message(f"Invalid absolute path.")
            sys.exit(1)

        # Read from 'trace.txt' to see if a path to some habit data exists
        try:
            with open(HAB_TRACE_FPATH, 'r') as f:
                absPath = f.readline()
        except OSError as err:
            display_error_message(f"OS Error: {err}")
            sys.exit(1)
        print(f"AB {absPath}")
        data = ''
        # Check if path within file exists. If it does exist, check if the user
        # path provided equals this file path to stop further execution. Record 
        # contents with the record data and afterwards remove it (IF the record
        # name is in the path. We shouldn't just delete a random file!)
        if absPath != '' and os.path.exists(absPath) and recordName in absPath:
            if userPath == absPath:
                display_error_message("Same paths.")
                sys.exit(1)
            try:
                # Capture data from record
                 with open(absPath, 'r') as fh:
                    data = json.load(fh)
            except json.JSONDecodeError as err:
                display_error_message(f"JSON decoding error: {err}")
                sys.exit(1)
            else:
                os.remove(absPath)

        # Attempt to store viable path for future use 
        try:
            with open(HAB_TRACE_FPATH, 'w') as f:
                f.write(viablePath)
        except OSError as err:
            display_error_message(f"OS Error: {err}")
            sys.exit(1)

         # Attempt to create record at given absolute user path 
        try:
            with open(viablePath, 'x') as fh:
                json.dump(data, fh, indent=HAB_JSON_IND)
        except OSError as err:
            display_error_message(f"OS Error: {err}")
            sys.exit(1)

        

#---Helper Methods----------------------------

    # Returns an index of the first found dict, else None
    def search_record_for_habit(self, key, data):
        return next( (i for i, habit in enumerate(data["habits"]) if habit["habit_name"] == key), None)


    def inquire_choice(self, choice:str):
        print(f"\n[habiter]  Are you sure you want to {choice}? This cannot be undone.\n")
        ans = ''
        while True:
            ans = input("[Provide a y/n.]: ")

            if ans != "y" and ans != "n":
                print("[err: INQUIRE_CHOICE] Please try again.")
            else:
                return True if ans == 'y' else False


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
