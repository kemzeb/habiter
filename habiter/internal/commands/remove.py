import sys
import click

from habiter.internal.utils.consts import HAB_TRACE_FPATH
from habiter.internal.utils.messenger import inquire_choice, echo_failure, echo_success
from habiter.internal.file.operations import SQLiteDataFileOperations


@click.command(short_help='delete habit(s) from record')
@click.argument('habits', required=True, nargs=-1)
def remove(habits):
    # Confirm user choice
    if inquire_choice("make a deletion") is False:
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
                fop.cur.execute('DELETE FROM habit WHERE habit_id=?',
                                (row['habit_id'],))
                echo_success(f"Habit \"{habit_name}\" has been deleted.")
