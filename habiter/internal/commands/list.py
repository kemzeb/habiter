import datetime as date
import json
import click

import habiter.internal.math as habmath
from habiter.internal.utils.consts import HAB_TRACE_FPATH, HAB_DATE_FORMAT
from habiter.internal.utils.messenger import display_message


@click.command(short_help='list all habits on record')
@click.option('-v', '--verbose', is_flag=True, default=False)
def list(verbose):
    # Read up-to-date record
    with open(HAB_TRACE_FPATH, 'r') as fh:
        data = json.load(fh)

    if verbose:
        list_verbose(data)
    else:
        list_reg(data)


def list_reg(data:dict) -> None:
    print("Habit\n-------------------")
    for habit in data["habits"]:
        print(habit["habit_name"])
    print("-------------------")


def list_verbose(data:dict) -> None:
    print("Habit + Attributes\t\t\tValue")
    print("-------------------\t\t\t-----")

    currDay = date.datetime.strptime(data["util"]["last_logged"], HAB_DATE_FORMAT).date()

    for habit in data["habits"]:
        deltaDay = None
        if habit["date_info"]["last_updated"] is not None:
            habitDay = date.datetime.strptime(habit["date_info"]["last_updated"], HAB_DATE_FORMAT).date()
            deltaDay = (currDay - habitDay).days  # subtraction returns a timedelta

        print("[{}]".format(habit["habit_name"]))
        prob = ((1 -
                 habmath.poisson_prob(habit["avg"], 0) -  # Prob. occurring never
                 habmath.poisson_prob(habit["avg"], 1)) * 100)  # Prob. occurring once
        probInfo = f"{prob:.3f}%" if habit["n_trials"] > 1 else "(More data required)"

        print(f"  | P(Occurrences >= 2 today):\t\t{probInfo}")

        print("  | Today's daily tally:\t\t{}".format(habit["occ"]))
        print("  | Total tally:\t\t\t{}".format(habit["total_occ"]))
        print("  | # of days captured:\t\t\t{}".format(habit["n_trials"]))
        print(f"  | Last updated:\t\t\t{deltaDay} day(s) ago")
        print("  | Date added:\t\t\t\t{}\n".format(habit["date_info"]["date_added"]))
    print("-------------------\t\t\t-----")
    display_message("Note: More data captured = increased statistical accuracy!\n")
