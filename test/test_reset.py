from click.testing import CliRunner

from habiter.internal.cli import habiter
from habiter.internal.file.operations import SQLiteDataFileOperations


def test_reset_with_non_existing_habit(setup, runner: CliRunner):
    result = runner.invoke(habiter, ["reset", "--yes", "t0"])
    assert result.exit_code == 1


def test_reset_on_existing_habit(setup, runner: CliRunner):
    runner.invoke(habiter, ["add", "t0"])

    with SQLiteDataFileOperations() as fo:
        # Populating habit with some values.
        fo.cur.execute(
            "UPDATE habit SET curr_tally = 5, "
            "total_tally = 30, num_of_trials = 4, "
            "wait_period = 1, is_active = True, "
            "prev_tally = 1 "
            'WHERE habit_name="t0"'
        )
    result = runner.invoke(habiter, ["reset", "--yes", "t0"])
    assert result.exit_code == 0

    with SQLiteDataFileOperations() as fo:
        fo.cur.execute('SELECT * FROM habit WHERE habit_name="t0"')
        row = fo.cur.fetchone()

        assert row["curr_tally"] == 0
        assert row["total_tally"] == 0
        assert row["num_of_trials"] == 0
        assert row["wait_period"] == 0
        assert row["is_active"] == 0
        assert row["prev_tally"] is None
