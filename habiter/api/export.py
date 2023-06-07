import csv
import os
import pathlib
from abc import ABC, abstractmethod

from platformdirs import user_data_dir

from habiter.internal.file.operations import SQLiteDataFileOperations
from habiter.internal.utils.consts import APP_AUTHOR, APP_NAME, DB_FILE_NAME


# TODO: Ensure this abstraction can be extended
class AbstractDataFileExport(ABC):
    def __init__(self, export_name: str, export_dir: str = os.getcwd()):
        self.export_name = export_name
        self.export_dir = export_dir

    @abstractmethod
    def export(self) -> None:
        """Export the habiter data file"""


class CSVExport(AbstractDataFileExport):
    def export(self) -> None:
        # TODO: We should abstract fetching the DB file path to a separate class.
        db_path = pathlib.Path(user_data_dir(APP_NAME, APP_AUTHOR)) / DB_FILE_NAME
        SQLiteDataFileOperations.set_f_path(db_path)

        with SQLiteDataFileOperations() as fo:
            # Retrieve all rows from database
            fo.cur.execute("SELECT * FROM habit")

            to_dir_path = os.path.join(self.export_dir, f"{self.export_name}.csv")
            with open(to_dir_path, "w") as csvfile:
                csv_writer = csv.writer(csvfile)

                # Retrieve columns
                # 'i[0]' because description returns a 7-tuple for each column
                csv_writer.writerow(i[0] for i in fo.cur.description)

                # Retrieve rows
                csv_writer.writerows(fo.cur)
