import sys
import click

from ._utils import abort_if_false
from habiter.internal.utils.messenger import (
    echo_failure, echo_success
)
from habiter.internal.file.operations import SQLiteDataFileOperations


@click.command(short_help='delete habit(s) from record')
@click.argument('habits', required=True, nargs=-1)
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to delete habit(s) from record?')
def remove(habits):
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
                fo.cur.execute('DELETE FROM habit WHERE habit_id=?',
                               (row['habit_id'],))
                echo_success(f"Habit \"{habit_name}\" has been deleted.")

        if non_existing_habit_detected:
            sys.exit(1)
