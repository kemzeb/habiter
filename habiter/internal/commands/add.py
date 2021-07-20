import click
import json

from habiter.internal.commands.utils import init_habit, search_record_for_habit
from habiter.internal.utils.consts import HAB_TRACE_FPATH, HAB_JSON_IND
from habiter.internal.utils.messenger import display_message, display_error_message


@click.command(short_help='add new habit(s) into record')
@click.argument('habits', required=True, nargs=-1)
def add(habits):
    # Cast to set to remove possible duplicates
    habits = set(habits)

    with open(HAB_TRACE_FPATH, 'r') as fh:
        data = json.load(fh)

    for arg in habits:
        # Search habit data for duplicates
        index = search_record_for_habit(arg, data)

        if index is None:
            newHabitObj = init_habit(arg)
            data["habits"].append(newHabitObj)
            display_message(f"Habit \"{arg}\" has been added.")
        else:
            display_error_message(f"Habit \"{arg}\" already exists.")

    with open(HAB_TRACE_FPATH, 'w') as fh:
        json.dump(data, fh, indent=HAB_JSON_IND)