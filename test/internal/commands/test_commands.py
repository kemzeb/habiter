import pytest
from click.testing import CliRunner

from habiter.internal.cli import habiter
from habiter.internal.file.operations import SQLiteDataFileOperations
from habiter.internal.file.creator import SQLiteDataFileCreator


@pytest.fixture
def temp_f_name() -> str:
    return "test.db"


@pytest.fixture
def temp_data_dir_path(tmpdir) -> str:
    return tmpdir.mkdir("test")


@pytest.fixture
def get_init_data_f_path(temp_data_dir_path, temp_f_name) -> str:
    SQLiteDataFileCreator(temp_data_dir_path, temp_f_name).create()
    return temp_data_dir_path.join(temp_f_name)


@pytest.fixture
def setup(get_init_data_f_path):
    SQLiteDataFileOperations.set_f_path(get_init_data_f_path)
    return SQLiteDataFileOperations.get_f_path()


def test_add(setup):
    runner = CliRunner()

    # Normal behavior
    result = runner.invoke(habiter, ["add", "t0", "t1"])
    assert result.exit_code == 0
    with SQLiteDataFileOperations() as fo:
        fo.cur.execute("SELECT habit_name FROM habit")
        rows = fo.cur.fetchall()
        assert rows[0]["habit_name"] in ["t0", "t1"]
        assert rows[1]["habit_name"] in ["t0", "t1"]

    # Add habit that already exists on record
    runner.invoke(habiter, ["add", "t2"])
    result = runner.invoke(habiter, ["add", "t2"])
    assert result.exit_code == 1
    with SQLiteDataFileOperations() as fo:
        fo.cur.execute("SELECT habit_name FROM habit " 'WHERE habit_name = "t2"')
        rows = fo.cur.fetchall()
        assert len(rows) < 2

    # Abnormal behavior (habit name is duplicated)
    result = runner.invoke(habiter, ["add", "t3", "t3"])
    assert result.exit_code == 0
    with SQLiteDataFileOperations() as fo:
        fo.cur.execute("SELECT habit_name FROM habit " 'WHERE habit_name = "t3"')
        rows = fo.cur.fetchall()
        assert len(rows) == 1


def test_list(setup):
    runner = CliRunner()

    # Print with empty record
    result = runner.invoke(habiter, ["list"])
    assert result.exit_code == 0

    # Print with habits in record
    runner.invoke(habiter, ["add", "t0", "t1"])
    result = runner.invoke(habiter, ["list"])
    assert result.exit_code == 0

    # Use verbose option
    result = runner.invoke(habiter, ["list", "-v"])
    assert result.exit_code == 0
    result = runner.invoke(habiter, ["list", "--verbose"])
    assert result.exit_code == 0

    # Provide existing habits as positional arguments
    result = runner.invoke(habiter, ["list", "t0", "t1", "-v"])
    assert result.exit_code == 0
    assert "[t0]" in result.output

    # Provide non-existing habits as positional arguments
    result = runner.invoke(habiter, ["list", "t1", "t99", "-v"])
    assert result.exit_code == 1
    assert "[t1]" in result.output


def test_remove(setup):
    runner = CliRunner()
    # Remove habit from an empty record
    result = runner.invoke(habiter, ["remove", "--yes", "t0"])
    assert result.exit_code == 1

    # Remove habit that exists on record
    runner.invoke(habiter, ["add", "t0"])
    runner.invoke(habiter, ["remove", "--yes", "t0"])

    with SQLiteDataFileOperations() as fo:
        fo.cur.execute('SELECT habit_name FROM habit WHERE habit_name="t0"')
        rows = fo.cur.fetchall()
        assert len(rows) == 0


def test_tally(setup):
    runner = CliRunner()
    # Tally habit that does not exist on record
    result = runner.invoke(habiter, ["tally", "t0"])
    assert result.exit_code == 1

    # Tally habit that does exist on record
    runner.invoke(habiter, ["add", "t0"])
    runner.invoke(habiter, ["tally", "t0"])
    with SQLiteDataFileOperations() as fo:
        fo.cur.execute('SELECT curr_tally FROM habit WHERE habit_name="t0"')
        row = fo.cur.fetchone()
        assert row["curr_tally"] == 1

    # Tally existing habit using '-n/--num' option
    runner.invoke(habiter, ["add", "t1"])
    runner.invoke(habiter, ["tally", "-n", 2, "t1"])
    runner.invoke(habiter, ["tally", "--num", 2, "t1"])
    with SQLiteDataFileOperations() as fo:
        fo.cur.execute('SELECT curr_tally FROM habit WHERE habit_name="t1"')
        row = fo.cur.fetchone()
        assert row["curr_tally"] == 4

    # Mark habit as active using '-z/--zero' option
    runner.invoke(habiter, ["add", "t2"])
    runner.invoke(habiter, ["tally", "-z", "t2"])
    runner.invoke(habiter, ["tally", "--zero", "t2"])
    with SQLiteDataFileOperations() as fo:
        # When a habit is added, it will by default be considered inactive
        # until the end user makes a tally, so we are testing to see if this
        # option marks it as active
        fo.cur.execute('SELECT is_active FROM habit WHERE habit_name="t2"')
        row = fo.cur.fetchone()
        assert row["is_active"]

    # Use the '-z/--zero' option' but the habit has already been active
    result = runner.invoke(habiter, ["tally", "-z", "t1"])
    assert result.exit_code == 1  # evaluates to a true expression


def test_reset(setup):
    runner = CliRunner()

    # Reset habit that does not exist on record
    result = runner.invoke(habiter, ["reset", "--yes", "t0"])
    assert result.exit_code == 1

    # Reset habit that exists on record
    runner.invoke(habiter, ["add", "t0"])
    with SQLiteDataFileOperations() as fo:
        # Reset habit that exists on record
        fo.cur.execute(
            "UPDATE habit SET curr_tally = 5, "
            "total_tally = 30, num_of_trials = 4, "
            "wait_period = 1, is_active = True, "
            "prev_tally = 1 "
            'WHERE habit_name="t0"'
        )
    runner.invoke(habiter, ["reset", "--yes", "t0"])
    with SQLiteDataFileOperations() as fo:
        fo.cur.execute('SELECT * FROM habit WHERE habit_name="t0"')
        row = fo.cur.fetchone()
    assert row["curr_tally"] == 0
    assert row["total_tally"] == 0
    assert row["num_of_trials"] == 0
    assert row["wait_period"] == 0
    assert row["is_active"] == 0
    assert row["prev_tally"] is None
