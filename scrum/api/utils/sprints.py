import datetime as dt
from typing import List

from scrum.db_models.sprint import Sprint


def has_intersecting_sprint(start_date: dt.date, all_sprints: List[Sprint], length: int = 2) -> bool:
    end_date = start_date + dt.timedelta(weeks=length)
    for db_sprint in all_sprints:
        has_any = (db_sprint.start_date <= start_date <= db_sprint.end_date or
                   db_sprint.start_date <= end_date <= db_sprint.end_date)
        if has_any:
            return True
    return False
