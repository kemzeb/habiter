import sys
import click
from datetime import datetime

from habiter.internal.utils.consts import HAB_DATE_FORMAT, HAB_TRACE_FPATH
from habiter.internal.utils.messenger import inquire_choice, echo_success, echo_failure
from habiter.internal.file.operations import SQLiteDataFileOperations


@click.command(short_help='reset some habit(s) from record')
@click.argument('habits', required=True, nargs=-1)
def reset(habits):
    # Confirm end user choice
    if inquire_choice("reset some habit(s)") is False:
        sys.exit(0)

    # Cast to set to remove possible duplicates
    habits = set(habits)

    with SQLiteDataFileOperations(HAB_TRACE_FPATH) as fop:

        for habit_name in habits:
            fop.cur.execute('SELECT habit_id FROM habit WHERE habit_name=?',
                            (habit_name,))
            row = fop.cur.fetchone()

            if row is None:
                echo_failure(f"No habit with the name \"{habit_name}\".")
            else:
                fop.cur.execute('UPDATE habit SET curr_tally = 0, '
                                'total_tally = 0, num_of_trials = 0, '
                                'wait_period = 0, is_active = False, '
                                'last_updated = ?, prev_tally = NULL '
                                'WHERE habit_id=?',
                                (datetime.now().strftime(HAB_DATE_FORMAT),
                                 row['habit_id']))
                echo_success(f"Habit \"{habit_name}\" has been reset.")
