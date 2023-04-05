import pytest
from click.testing import CliRunner

from habiter.internal.file.creator import SQLiteDataFileCreator
from habiter.internal.file.operations import SQLiteDataFileOperations


@pytest.fixture(scope="session")
def session_setup(tmp_path_factory) -> None:
    temp_db_dir_path = tmp_path_factory.mktemp("habiter")
    temp_db_file_name = "test.db"
    temp_db_file_path = temp_db_dir_path / temp_db_file_name

    SQLiteDataFileCreator(temp_db_dir_path, temp_db_file_name).create()
    SQLiteDataFileOperations.set_f_path(temp_db_file_path)


@pytest.fixture
def setup(session_setup) -> None:
    yield

    with SQLiteDataFileOperations() as fo:
        fo.cur.execute("DELETE FROM habit")


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()
