import sys
import click
import json

from habiter.internal.commands.utils import search_record_for_habit
from habiter.internal.utils.consts import HAB_TRACE_FPATH, HAB_JSON_IND
from habiter.internal.utils.messenger import inquire_choice, display_error_message, display_message


@click.command(short_help='delete habit(s) from record')
@click.argument('habits', required=True, nargs=-1)
def remove(habits):
    # Cast to set to remove possible duplicates
    habits = set(habits)

    # Confirm user choice
    if inquire_choice("make a deletion") is False:
        sys.exit(0)

    # Read up-to-date record
    with open(HAB_TRACE_FPATH, 'r') as fh:
        data = json.load(fh)

        if len(data["habits"]) <= 0:
            display_error_message("Cannot delete from an empty habit list.")
        else:
            for arg in habits:
                index = search_record_for_habit(arg, data)

                if index != None:
                    data["habits"].pop(index)  # Remove dict from "habits" list
                    display_message(f"Habit \"{arg}\" has been deleted.")
                else:
                    display_error_message(f"No habit with the name \"{arg}\".")

       # Write new data to .json file
        with open(HAB_TRACE_FPATH, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)