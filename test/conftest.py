import pytest
from click.testing import CliRunner

from habiter.internal.file.creator import SQLiteDataFileCreator
from habiter.internal.file.operations import SQLiteDataFileOperations


@pytest.fixture
def setup(tmpdir) -> None:
    temp_db_dir_path = tmpdir.mkdir("test")
    temp_db_file_name = "test.db"
    temp_db_file_path = temp_db_dir_path.join(temp_db_file_name)
    
    SQLiteDataFileCreator(temp_db_dir_path, temp_db_file_name).create()
    SQLiteDataFileOperations.set_f_path(temp_db_file_path)


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()
