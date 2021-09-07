import sys
import click
from datetime import datetime

from habiter.internal.utils.consts import HAB_DATE_FORMAT
from habiter.internal.utils.messenger import echo_success, echo_failure
from habiter.internal.file.operations import SQLiteDataFileOperations


@click.command(short_help='add new habit(s) into record')
@click.argument('habits', required=True, nargs=-1)
def add(habits):
    existing_habit_detected = False

    # Cast to set to remove possible duplicates
    habits = set(habits)

    with SQLiteDataFileOperations() as fo:

        # TODO: Instead of invoking a query on each habit_name, try to use one query for all habits
        for habit_name in habits:
            fo.cur.execute('SELECT curr_tally, prev_tally, is_active, '
                           'last_updated, num_of_trials FROM habit WHERE '
                           'habit_name=?', (habit_name,))
            row = fo.cur.fetchone()
            if row is not None:
                existing_habit_detected = True
                echo_failure(f"Habit \"{habit_name}\" already exists.")
                continue
            curr_time = datetime.now().strftime(HAB_DATE_FORMAT)
            fo.cur.execute(
                'INSERT INTO habit (habit_name, curr_tally, '
                'total_tally, num_of_trials, wait_period, is_active, '
                'last_updated, date_added) '
                'VALUES(?, 0, 0, 0, 0, False, ?, ?)',
                (habit_name, curr_time, curr_time))
            echo_success(f"Habit \"{habit_name}\" has been added.")

        if existing_habit_detected:
            sys.exit(1)
