from click.testing import CliRunner

from habiter.internal.cli import habiter
from habiter.internal.file.operations import SQLiteDataFileOperations


def test_add_normal_add(setup, runner: CliRunner):
    result = runner.invoke(habiter, ["add", "t0", "t1"])
    assert result.exit_code == 0

    with SQLiteDataFileOperations() as fo:
        fo.cur.execute("SELECT habit_name FROM habit")
        rows = fo.cur.fetchall()
        assert rows[0]["habit_name"] in ["t0", "t1"]
        assert rows[1]["habit_name"] in ["t0", "t1"]


def test_add_with_habit_that_already_exists(setup, runner):
    runner.invoke(habiter, ["add", "t2"])
    result = runner.invoke(habiter, ["add", "t2"])
    assert result.exit_code == 1

    with SQLiteDataFileOperations() as fo:
        fo.cur.execute("SELECT habit_name FROM habit WHERE habit_name = 't2'")
        rows = fo.cur.fetchall()
        assert len(rows) < 2
