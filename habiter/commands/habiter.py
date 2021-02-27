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

from habiter.utils.messenger import (
display_message,
display_error_message,
)
from habiter.utils.constants import (
    HAB_DIR_FPATH,
    HAB_TRACE_FPATH,
    HAB_DATE_FORMAT,
    HAB_JSON_IND,
    HABITER_VERSION,
)
from habiter.upkeep.updater import HabiterUpdater


class Habiter:
    def __init__(self):

        # Update user habit data
        HabiterUpdater()


    def tally_habits(self, args, numOfOcc = 1):
        # Cast to set to remove possible duplicates
        args = set(args)

        # Read up-to-date record
        with open(HAB_TRACE_FPATH, 'r') as fh:
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
        with open(HAB_TRACE_FPATH, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)


    def add_habits(self, *args):
        # Cast to set to remove possible duplicates
        args = set(args)

        with open(HAB_TRACE_FPATH, 'r') as fh:
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

        with open(HAB_TRACE_FPATH, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)


    def delete_habits(self, *args):
        # Cast to set to remove possible duplicates
        args = set(args)

        # Confirm user choice
        if self.inquire_choice("make a deletion") is False:
            sys.exit(0)

        # Read up-to-date record
        with open(HAB_TRACE_FPATH, 'r') as fh:
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
        with open(HAB_TRACE_FPATH, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)


    def reset_habits(self, *args):
        # Cast to set to remove possible duplicates
        args = set(args)

        # Confirm end user choice
        if self.inquire_choice("reset some habit(s)") is False:
            sys.exit(0)

        # Read up-to-date record
        with open(HAB_TRACE_FPATH, 'r') as fh:
            data = json.load(fh)

        for arg in args:
            index = self.search_record_for_habit(arg, data)

            if index != None:
                dateAdded = data["habits"][index]["date_info"]["date_added"]
                data["habits"][index] = self.init_habit(arg, dateAdded)

                display_message(f"Habit \"{arg}\" has been reset.")
            else:
                display_error_message(f"No habit with the name \"{arg}\".")

        with open(HAB_TRACE_FPATH, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)


    def list_habits(self):
        # Read up-to-date record
        with open(HAB_TRACE_FPATH, 'r') as fh:
            data = json.load(fh)

        print("Habit\n-------------------")
        for habit in data["habits"]:
            print(habit["habit_name"])
        print("-------------------")


    def list_habits_k(self):
        # Read up-to-date record
        with open(HAB_TRACE_FPATH, 'r') as fh:
            data = json.load(fh)

        print("Habit + Attributes\t\t\tValue")
        print("-------------------\t\t\t-----")

        currDay = date.datetime.strptime(data["util"]["last_logged"], HAB_DATE_FORMAT).date()

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
        with open(HAB_TRACE_FPATH, 'r') as fh:
            data = json.load(fh)

        print("Habit\n-------------------")
        for habit in data["habits"]:
            prob = ((1 - habmath.poisson_prob(habit["avg"], 0) -      # Prob. occurring never
                         habmath.poisson_prob(habit["avg"], 1)) * 100) # Prob. occuring once
            print(habit["habit_name"])
            print(f"  | P(X >= 2) = {probability:.3f}%")
        print("-------------------")

#---Main Options-----------------------------
# No main CLI option methods exists as of yet

#---Helper Methods----------------------------

    # Returns an index of the first found dict, else None
    def search_record_for_habit(self, key, data):
        return next( (i for i, habit in enumerate(data["habits"]) \
                                     if habit["habit_name"] == key), None)


    def inquire_choice(self, choice:str):
        display_message(f"Are you sure you want to {choice}? This cannot be undone.\n")
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
