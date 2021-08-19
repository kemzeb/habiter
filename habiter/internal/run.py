#!/usr/bin/env python3

"""
'   The entry point of habiter
"""

import os

import habiter.internal.cli as cli
from habiter.internal.file.creator import SQLiteDataFileCreator
from habiter.internal.file.updater import SQLiteDataFileUpdater
from habiter.internal.file.operations import SQLiteDataFileOperations

from habiter.internal.utils.consts import (
    HAB_FDATA, HAB_DIR_FPATH
)


def main():
    data_file_creator = SQLiteDataFileCreator(HAB_DIR_FPATH, HAB_FDATA)
    data_file_creator.create()
    data_file_path = data_file_creator.get_data_file_path()

    # Instantiate singleton for operations conducted on data file
    SQLiteDataFileOperations(data_file_path)

    data_file_updater = SQLiteDataFileUpdater(data_file_path)
    data_file_updater.update()

    cli.habiter()


if __name__ == "__main__":
    main()
