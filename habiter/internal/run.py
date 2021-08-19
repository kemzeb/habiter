#!/usr/bin/env python3

"""
'   The entry point of habiter
"""

import os

from appdirs import user_data_dir

import habiter.internal.cli as cli
from habiter.internal.file.creator import SQLiteDataFileCreator
from habiter.internal.file.updater import SQLiteDataFileUpdater
from habiter.internal.file.operations import SQLiteDataFileOperations

from habiter.internal.utils.consts import (
    HAB_AUTHOR, HAB_NAME, HAB_F_RECORD_NAME
)


def main():
    dir_path = user_data_dir(HAB_NAME, HAB_AUTHOR)
    data_file_creator = SQLiteDataFileCreator(dir_path, HAB_F_RECORD_NAME)
    data_file_creator.create()
    data_file_path = data_file_creator.get_data_f_path()

    # Set the data file path that all classes using this can have access to
    SQLiteDataFileOperations().set_f_path(data_file_path)

    data_file_updater = SQLiteDataFileUpdater(data_file_path)
    data_file_updater.update()

    cli.habiter()


if __name__ == "__main__":
    main()
