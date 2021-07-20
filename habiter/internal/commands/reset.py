import sys
import click
import json

from habiter.internal.commands.utils import search_record_for_habit, init_habit
from habiter.internal.utils.consts import HAB_TRACE_FPATH, HAB_JSON_IND
from habiter.internal.utils.messenger import inquire_choice, echo_success, echo_failure


@click.command(short_help='reset some habit(s) from record')
@click.argument('habits', required=True, nargs=-1)
def reset(habits):
    # Cast to set to remove possible duplicates
    habits = set(habits)

    # Confirm end user choice
    if inquire_choice("reset some habit(s)") is False:
        sys.exit(0)

    # Read up-to-date record
    with open(HAB_TRACE_FPATH, 'r') as fh:
        data = json.load(fh)

    for arg in habits:
        index = search_record_for_habit(arg, data)

        if index != None:
            dateAdded = data["habits"][index]["date_info"]["date_added"]
            data["habits"][index] = init_habit(arg, dateAdded)

            echo_success(f"Habit \"{arg}\" has been reset.")
        else:
            echo_failure(f"No habit with the name \"{arg}\".")

    with open(HAB_TRACE_FPATH, 'w') as fh:
        json.dump(data, fh, indent=HAB_JSON_IND)
