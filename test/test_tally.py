from click.testing import CliRunner

from habiter.internal.cli import habiter
from habiter.internal.file.operations import SQLiteDataFileOperations


def test_tally_non_existing_habit(setup, runner: CliRunner):
    result = runner.invoke(habiter, ["tally", "t0"])
    assert result.exit_code == 1


def test_tally_existing_habit(setup, runner: CliRunner):
    runner.invoke(habiter, ["add", "t0"])
    runner.invoke(habiter, ["tally", "t0"])
    with SQLiteDataFileOperations() as fo:
        fo.cur.execute('SELECT curr_tally FROM habit WHERE habit_name="t0"')
        row = fo.cur.fetchone()
        assert row["curr_tally"] == 1


def test_tally_existing_habit_using_num_option(setup, runner: CliRunner):
    runner.invoke(habiter, ["add", "t1"])

    result = runner.invoke(habiter, ["tally", "-n", 2, "t1"])
    assert result.exit_code == 0

    result = runner.invoke(habiter, ["tally", "--num", 2, "t1"])
    assert result.exit_code == 0

    with SQLiteDataFileOperations() as fo:
        fo.cur.execute('SELECT curr_tally FROM habit WHERE habit_name="t1"')
        row = fo.cur.fetchone()
        assert row["curr_tally"] == 4


def test_tally_using_zero_option_on_inactive_habit(setup, runner: CliRunner):
    # By default, a newly-added habit is considered inactive.
    runner.invoke(habiter, ["add", "t2"])

    result = runner.invoke(habiter, ["tally", "-z", "t2"])
    assert result.exit_code == 0

    result = runner.invoke(habiter, ["tally", "--zero", "t2"])
    assert result.exit_code == 0

    with SQLiteDataFileOperations() as fo:
        # When a habit is added, it will by default be considered inactive
        # until the end user makes a tally, so we are testing to see if this
        # option marks it as active.
        fo.cur.execute('SELECT is_active FROM habit WHERE habit_name="t2"')
        row = fo.cur.fetchone()
        assert row["is_active"]


def test_tally_using_zero_option_but_habit_already_active(setup, runner: CliRunner):
    runner.invoke(habiter, ["add", "t1"])
    runner.invoke(habiter, ["tally", "t1"])

    result = runner.invoke(habiter, ["tally", "-z", "t1"])
    assert result.exit_code == 1
