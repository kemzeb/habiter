import datetime as date

from habiter.internal.utils.consts import HAB_DATE_FORMAT


def search_record_for_habit(key, data):
    return next((i for i, habit in enumerate(data["habits"]) \
                 if habit["habit_name"] == key), None)


def init_habit(habitName: str,
               dateAdded=date.datetime.now().strftime(HAB_DATE_FORMAT)):
    ''' Initalizes a dict to be stored in the habit data

    Parameters
        habitName:  name of the habit to be added
        date:       date that it was added
    '''
    return {
        "habit_name": habitName,
        "occ": 0,
        "total_occ": 0,
        "prev_occ": None,
        "n_trials": 0,
        "avg": 0.0,
        "date_info":
            {
                "date_added": dateAdded,
                "last_updated": None,
                "active": False
            }
    }
