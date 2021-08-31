import pytest
from click.testing import CliRunner


from habiter.internal.cli import habiter
from habiter.internal.file.operations import SQLiteDataFileOperations
from habiter.internal.file.creator import SQLiteDataFileCreator

# TODO: We may need to test for multiple habit name inputs for the commands that take them


@pytest.fixture
def temp_f_name() -> str:
    return 'test.db'


@pytest.fixture
def temp_data_dir_path(tmpdir) -> str:
    return tmpdir.mkdir('test')


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
    result = None

    with SQLiteDataFileOperations() as fo:
        # Normal behavior
        result = runner.invoke(habiter, ['add', 't0', 't1'])
        assert result.exit_code == 0

        fo.cur.execute('SELECT habit_name FROM habit')
        rows = fo.cur.fetchall()
        assert rows[0]['habit_name'] in ['t0', 't1']
        assert rows[1]['habit_name'] in ['t0', 't1']

        # Add habit that already exists on record)
        runner.invoke(habiter, ['add', 't2'])
        result = runner.invoke(habiter, ['add', 't2'])
        assert result.exit_code == 0

        fo.cur.execute('SELECT habit_name FROM habit '
                       'WHERE habit_name = "t2"')
        rows = fo.cur.fetchall()
        assert len(rows) < 2

        # Abnormal behavior (habit name is duplicated)
        result = runner.invoke(habiter, ['add', 't3', 't3'])
        assert result.exit_code == 0

        fo.cur.execute('SELECT habit_name FROM habit '
                       'WHERE habit_name = "t3"')
        rows = fo.cur.fetchall()
        assert len(rows) == 1


def test_list(setup):
    runner = CliRunner()
    result = None

    with SQLiteDataFileOperations() as fo:
        # Print with empty record)
        result = runner.invoke(habiter, ['list'])
        assert result.exit_code == 0

        # Print with habits in record)
        runner.invoke(habiter, ['add', 't0', 't1'])
        result = runner.invoke(habiter, ['list'])
        assert result.exit_code == 0

        # Use verbose option
        result = runner.invoke(habiter, ['list', '-v'])
        assert result.exit_code == 0
        result = runner.invoke(habiter, ['list', '--verbose'])
        assert result.exit_code == 0


def test_remove(setup):
    runner = CliRunner()
    result = None

    with SQLiteDataFileOperations() as fo:
        # Remove habit from an empty record
        result = runner.invoke(habiter, ['remove', '--yes', 't0'])
        assert result.output == '[habiter: error]  No habit with the name "t0".\n'

        # Remove habit that exists on record
        runner.invoke(habiter, ['add', 't0'])
        runner.invoke(habiter, ['remove', '--yes', 't0'])
        fo.cur.execute('SELECT habit_name FROM habit WHERE habit_name="t0"')
        rows = fo.cur.fetchall()
        assert len(rows) == 0


def test_tally(setup):
    runner = CliRunner()
    result = None

    with SQLiteDataFileOperations() as fo:
        # Tally habit that does not exist on record
        result = runner.invoke(habiter, ['tally', 't0'])
        assert result.output == '[habiter: error]  No habit with the name "t0".\n'

        # Tally habit that does exist on record
        runner.invoke(habiter, ['add', 't0'])
        runner.invoke(habiter, ['tally', 't0'])
        fo.cur.execute('SELECT curr_tally FROM habit WHERE habit_name="t0"')
        row = fo.cur.fetchone()
        assert row['curr_tally'] == 1

        # Tally existing habit using '-n/--num' option
        runner.invoke(habiter, ['add', 't1'])
        runner.invoke(habiter, ['tally', '-n', 2, 't1'])
        runner.invoke(habiter, ['tally', '--num', 2, 't1'])
        fo.cur.execute('SELECT curr_tally FROM habit WHERE habit_name="t1"')
        row = fo.cur.fetchone()
        assert row['curr_tally'] == 4

        # Mark habit as active using '-z/--zero' option
        runner.invoke(habiter, ['add', 't2'])
        runner.invoke(habiter, ['tally', '-z', 't2'])
        result = runner.invoke(habiter, ['tally', '--zero', 't2'])

        # When a habit is added, it will by default be considered inactive
        # until the end user makes a tally, so we are testing to see if this
        # option marks it as active
        fo.cur.execute('SELECT is_active FROM habit WHERE habit_name="t2"')
        row = fo.cur.fetchone()
        assert row['is_active'] == True

        # Use the '-z/--zero' option' but the habit has already been active
        result = runner.invoke(habiter, ['tally', '-z', 't1'])
        assert result.output == '[habiter: error]  Habit "t1" contains occurrences.\n'


def test_reset(setup):
    runner = CliRunner()
    result = None

    with SQLiteDataFileOperations() as fo:
        # Reset habit that does not exist on record
        result = runner.invoke(habiter, ['reset', '--yes', 't0'])
        assert result.output == '[habiter: error]  No habit with the name "t0".\n'

        # Reset habit that exists on record
        runner.invoke(habiter, ['add', 't0'])
        runner.invoke(habiter, ['tally', '-n', 3, 't0'])
        runner.invoke(habiter, ['reset', '--yes', 't0'])
        fo.cur.execute('SELECT curr_tally FROM habit WHERE habit_name="t0"')
        row = fo.cur.fetchone()
        assert row['curr_tally'] == 0
