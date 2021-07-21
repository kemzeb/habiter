import json
import datetime as date
import click

from habiter.internal.commands.utils import search_record_for_habit
from habiter.internal.utils.consts import HAB_TRACE_FPATH, HAB_JSON_IND, HAB_DATE_FORMAT
from habiter.internal.utils.messenger import echo_failure, echo_success


@click.command(short_help='increment the number of occurrences for some habit(s)')
@click.argument('habits', required=True, nargs=-1)
@click.option('-n', '--num', default=1)
@click.option('-z', '--zero', is_flag=True)
def tally(habits, num, zero):
    # Cast to set to remove possible duplicates
    habits = set(habits)

    # Read up-to-date record
    with open(HAB_TRACE_FPATH, 'r') as fh:
        data = json.load(fh)

    for arg in habits:
        index = search_record_for_habit(arg, data)  # search for index matching current habit name

        if index is not None:
            # Check it the '--zero' flag has been used and has there already been tallies captured
            if zero and data["habits"][index]["occ"] > 0:
                echo_failure(f"Habit \"{arg}\" contains occurrences.")
                continue

            # Update habit data
            habit = data["habits"][index]
            habit["prev_occ"] = habit["occ"]  # Capture previous tally
            habit["occ"] += num
            habit["total_occ"] += num

            # Update date information
            habit["date_info"]["last_updated"] = f"{date.datetime.now().strftime(HAB_DATE_FORMAT)}"
            habit["date_info"]["active"] = True

            data["habits"][index] = habit

            echo_success("Habit \"{}\" tally updated from {} to {}.".format(arg,
                                                                            habit["prev_occ"],
                                                                            habit["occ"]))
        else:
            echo_failure(f"Habit \"{arg}\" does not exist.")

    # Write new data to .json file
    with open(HAB_TRACE_FPATH, 'w') as fh:
        json.dump(data, fh, indent=HAB_JSON_IND)
