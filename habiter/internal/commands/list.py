import sqlite3
import sys
from datetime import datetime

import click

from habiter.internal.file.operations import SQLiteDataFileOperations
from habiter.internal.math import poisson_prob
from habiter.internal.utils.consts import DB_DATE_FORMAT
from habiter.internal.utils.messenger import echo_failure, echo_info


@click.command(short_help="list all habits on record")
@click.option("-l", "--less", is_flag=True, default=False)
@click.argument("habits", nargs=-1, required=False)
def list(habits, less):
    non_existing_habit_detected = False
    data = []
    habits = set(habits)  # Cast to set to remove possible duplicates
    with SQLiteDataFileOperations() as fo:
        if len(habits) != 0:
            for habit_name in habits:
                fo.cur.execute(
                    "SELECT * FROM habit WHERE " "habit_name=?", (habit_name,)
                )
                row = fo.cur.fetchone()
                if row is None:
                    non_existing_habit_detected = True
                    echo_failure(f'Habit "{habit_name}" does not exist.')
                    continue
                data.append(row)
        else:
            data = fo.cur.execute("SELECT * FROM habit").fetchall()
        meta_data = fo.cur.execute("SELECT last_logged FROM meta_info").fetchone()
    if less:
        print("Habit\n-------------------")
        for habit in data:
            print(habit["habit_name"])
        print("-------------------")
    else:
        last_logged_date = datetime.strptime(
            meta_data["last_logged"], DB_DATE_FORMAT
        ).date()
        print("Habit + Attributes\t\t\tValue")
        print("-------------------\t\t\t-----")
        for habit in data:
            print_verbose(habit, last_logged_date)
        print("-------------------\t\t\t-----")
        echo_info("Note: More data captured = increased statistical accuracy!\n")
    if non_existing_habit_detected:
        sys.exit(1)


def print_verbose(habit: sqlite3.Row, logged_date):
    last_habit_update = datetime.strptime(habit["last_updated"], DB_DATE_FORMAT).date()
    delta_day = (logged_date - last_habit_update).days

    print("[{}]".format(habit["habit_name"]))
    if habit["num_of_trials"] < 2:
        prob_text = "(More data required)"
    else:
        avg = habit["total_tally"] / habit["num_of_trials"]
        prob = (1 - poisson_prob(avg, 0) - poisson_prob(avg, 1)) * 100
        prob_text = f"{prob:.3f}%"

    print(f"  | P(Occurrences > 1 today):\t\t{prob_text}")
    print("  | Today's daily tally:\t\t{}".format(habit["curr_tally"]))
    print("  | Total tally:\t\t\t{}".format(habit["total_tally"]))
    print("  | # of days captured:\t\t\t{}".format(habit["num_of_trials"]))
    print(f"  | Last updated:\t\t\t{delta_day} day(s) ago")
    print("  | Date added:\t\t\t\t{}\n".format(habit["date_added"]))
