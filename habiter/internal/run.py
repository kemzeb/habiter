#!/usr/bin/env python3

"""
'   The entry point of habiter
"""

import os

import habiter.internal.cli as cli
from habiter.internal.file.creator import SQLiteDataFileCreator
from habiter.internal.file.updater import SQLiteDataFileUpdater
from habiter.internal.utils.consts import (
    HAB_FDATA, HAB_DIR_FPATH
)


def main():
    SQLiteDataFileCreator().create(HAB_DIR_FPATH, HAB_FDATA)

    data_file_path = os.path.join(HAB_DIR_FPATH, HAB_FDATA)
    SQLiteDataFileUpdater().update(data_file_path)
    cli.habiter()


if __name__ == "__main__":
    main()
