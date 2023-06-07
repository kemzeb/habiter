import sys
from datetime import datetime

import click

from habiter.internal.file.operations import SQLiteDataFileOperations
from habiter.internal.utils.consts import DB_DATE_FORMAT
from habiter.internal.utils.messenger import echo_failure, echo_success, echo_warning


@click.command(short_help="increment the number of occurrences for some habit(s)")
@click.argument("habits", required=True, nargs=-1)
@click.option("-n", "--num", default=1)
@click.option("-z", "--zero", is_flag=True)
def tally(habits, num, zero):
    flag = False

    # Cast to set to remove possible duplicates
    habits = set(habits)

    with SQLiteDataFileOperations() as fo:
        for habit_name in habits:
            fo.cur.execute(
                "SELECT habit_id, curr_tally, total_tally "
                "FROM habit WHERE habit_name=?",
                (habit_name,),
            )
            row = fo.cur.fetchone()
            if row:
                if zero:
                    if row["curr_tally"] > 0:
                        echo_failure(
                            f'Habit "{habit_name}" already contains occurrences.'
                        )
                        flag = True
                        continue
                    # If a number was passed, make sure to inform the end user
                    # that the number given will be ignored.
                    if num != 1:
                        echo_warning("--zero flag passed; ignoring --num value.")
                    num = 0

                prev_tally = row["curr_tally"]
                curr_tally = row["curr_tally"] + num
                total_tally = row["total_tally"] + num
                is_active = True
                last_updated = datetime.now().strftime(DB_DATE_FORMAT)

                fo.cur.execute(
                    "UPDATE habit SET curr_tally=?, "
                    "total_tally=?, is_active=?, "
                    "last_updated=?, prev_tally=? "
                    "WHERE habit_id = ?",
                    (
                        curr_tally,
                        total_tally,
                        is_active,
                        last_updated,
                        prev_tally,
                        row["habit_id"],
                    ),
                )
                if zero:
                    echo_success(f'Habit "{habit_name}" marked as active.')
                else:
                    echo_success(
                        f'Habit "{habit_name}" tally updated '
                        f"from {prev_tally} to {curr_tally}."
                    )
            else:
                echo_failure(f'No habit with the name "{habit_name}".')
                flag = True

        if flag:
            sys.exit(1)
