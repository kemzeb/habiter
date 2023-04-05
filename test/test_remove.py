from click.testing import CliRunner

from habiter.internal.cli import habiter
from habiter.internal.file.operations import SQLiteDataFileOperations


def test_remove_habit_from_empty_record(setup, runner: CliRunner):
    result = runner.invoke(habiter, ["remove", "--yes", "t0"])
    assert result.exit_code == 1


def test_remove_existing_habit(setup, runner: CliRunner):
    runner.invoke(habiter, ["add", "t0"])
    result = runner.invoke(habiter, ["remove", "--yes", "t0"])
    assert result.exit_code == 0

    with SQLiteDataFileOperations() as fo:
        fo.cur.execute('SELECT habit_name FROM habit WHERE habit_name="t0"')
        rows = fo.cur.fetchall()
        assert len(rows) == 0
