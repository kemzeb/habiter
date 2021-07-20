import sys
import click
import json

from habiter.internal.commands.utils import search_record_for_habit
from habiter.internal.utils.consts import HAB_TRACE_FPATH, HAB_JSON_IND
from habiter.internal.utils.messenger import inquire_choice, echo_failure, echo_success


@click.command(short_help='delete habit(s) from record')
@click.argument('habits', required=True, nargs=-1)
def remove(habits):
    # Confirm user choice
    if inquire_choice("make a deletion") is False:
        sys.exit(0)

    # Cast to set to remove possible duplicates
    habits = set(habits)

    # Read up-to-date record
    with open(HAB_TRACE_FPATH, 'r') as fh:
        data = json.load(fh)

        if len(data["habits"]) < 1:
            echo_failure("Cannot delete from an empty habit list.")
        else:
            for arg in habits:
                index = search_record_for_habit(arg, data)

                if index != None:
                    data["habits"].pop(index)  # Remove dict from "habits" list
                    echo_success(f"Habit \"{arg}\" has been deleted.")
                else:
                    echo_failure(f"No habit with the name \"{arg}\".")

       # Write new data to .json file
        with open(HAB_TRACE_FPATH, 'w') as fh:
            json.dump(data, fh, indent=HAB_JSON_IND)