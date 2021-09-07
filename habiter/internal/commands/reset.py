import sys
import click
from datetime import datetime

from ._utils import abort_if_false
from habiter.internal.utils.consts import HAB_DATE_FORMAT
from habiter.internal.utils.messenger import echo_success, echo_failure
from habiter.internal.file.operations import SQLiteDataFileOperations


@click.command(short_help='reset some habit(s) from record')
@click.argument('habits', required=True, nargs=-1)
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to reset habit(s) from record?')
def reset(habits):
    non_existing_habit_detected = False

    # Cast to set to remove possible duplicates
    habits = set(habits)

    with SQLiteDataFileOperations() as fo:

        for habit_name in habits:
            fo.cur.execute('SELECT habit_id FROM habit WHERE habit_name=?',
                           (habit_name,))
            row = fo.cur.fetchone()

            if row is None:
                echo_failure(f"No habit with the name \"{habit_name}\".")
                non_existing_habit_detected = True
            else:
                fo.cur.execute('UPDATE habit SET curr_tally = 0, '
                               'total_tally = 0, num_of_trials = 0, '
                               'wait_period = 0, is_active = False, '
                               'last_updated = ?, prev_tally = NULL '
                               'WHERE habit_id=?',
                               (datetime.now().strftime(HAB_DATE_FORMAT),
                                row['habit_id']))
                echo_success(f"Habit \"{habit_name}\" has been reset.")

        if non_existing_habit_detected:
            sys.exit(1)
