
from datetime import datetime
from typing import Dict, List

import babel
from dateutil import parser
from flask_sqlalchemy.model import Model
from sqlalchemy import inspect


def format_datetime(value: str, format: str = "medium") -> str:
    date = parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


def model_to_dict(obj: Model) -> Dict:
    results = dict()
    for col in inspect(obj).mapper.column_attrs:
        value = getattr(obj, col.key)
        if isinstance(value, datetime):
            results[col.key] = value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            results[col.key] = value
    return results


def compose_show_attributes(shows: List[Model]) -> Dict:
    past_shows = list(filter(lambda show: show.start_time <= datetime.now(), shows))
    upcoming_shows = list(filter(lambda show: show.start_time > datetime.now(), shows))

    return {
        "past_shows": [model_to_dict(show) for show in past_shows],
        "upcoming_shows": [model_to_dict(show) for show in upcoming_shows],
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }


def filter_dict_by_keys(input_dict: Dict, keep_keys: List) -> Dict:
    return {key: value for key, value in input_dict.items() if key in keep_keys}
