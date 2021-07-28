import os

from appdirs import user_data_dir

HAB_DATE_FORMAT = "%d %b, %Y %H:%M%p"
HAB_JSON_IND = 2

# Data retrieval
HAB_NAME = 'habiter'
HAB_AUTHOR = 'kemzeb'
HAB_FDATA = 'records.json'

# TODO: Probably should not consider file paths as constants, especially down the line when new features are implemented
HAB_DIR_FPATH = user_data_dir(HAB_NAME, HAB_AUTHOR)
# .. full path without user habit data file

HAB_TRACE_FPATH = os.path.join(HAB_DIR_FPATH, HAB_FDATA)
# .. full path with user habit data included
