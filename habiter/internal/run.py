#!/usr/bin/env python3

"""
'   The entry point of habiter
"""

from platformdirs import user_data_dir

import habiter.internal.cli as cli
from habiter.internal.file.creator import SQLiteDataFileCreator
from habiter.internal.file.updater import SQLiteDataFileUpdater
from habiter.internal.file.operations import SQLiteDataFileOperations

from habiter.internal.utils.consts import APP_AUTHOR, APP_NAME, DB_FILE_NAME


def main():
    dir_path = user_data_dir(APP_NAME, APP_AUTHOR)
    creator = SQLiteDataFileCreator(dir_path, DB_FILE_NAME)
    creator.create()
    data_file_path = creator.get_data_file_path()

    # Set the data file path that all classes using this can have access to.
    SQLiteDataFileOperations.set_f_path(data_file_path)

    updater = SQLiteDataFileUpdater(data_file_path)
    updater.update()

    cli.habiter()


if __name__ == "__main__":
    main()
