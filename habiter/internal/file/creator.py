"""
This file contains implementations involving
the creation of files used to r/w data
"""

import os
import datetime as date
import json
import appdirs

from abc import ABC, abstractmethod

from habiter import __version__

from habiter.internal.utils.consts import HAB_DATE_FORMAT, HAB_JSON_IND


class AbstractFileCreator(ABC):
    """An abstract class that defines file creation behaviors"""

    def create(self, dir_path: str, f_name: str) -> None:
        """Creates a file with directory path that is also created if needed

        Parameters
        ----------
        dir_path: str
            The directory path in which the file will reside
        f_name: str
            The name of the file
        """
        # Determine if user data directory exists
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        data_file_path = os.path.join(dir_path, f_name)
        if not os.path.isfile(data_file_path):
            self._init_file(data_file_path)

    @abstractmethod
    def _init_file(self, f_path: str) -> None:
        """Abstract method that creates and initializes the contents of a file

        Parameters
        ----------
        f_path: str
            File path to the file that is to be created
        """
        pass


class JSONDataFileCreator(AbstractFileCreator):

    def _init_file(self, f_path: str) -> None:
        with open(f_path, 'w') as f:
            # Initialize JSON arrays to hold JSON objects
            initFileContents = {
                "util": {
                    "version": __version__,
                    "last_logged": date.datetime.now().strftime(HAB_DATE_FORMAT)
                },
                "habits": []
            }
            json.dump(initFileContents, f, indent=HAB_JSON_IND)
