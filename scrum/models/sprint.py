import datetime as dt
from typing import Optional

from pydantic import BaseModel


class SprintBase(BaseModel):
    start_date: dt.date
    project_id: int


class SprintBaseInDb(SprintBase):
    id: int
    end_date: dt.date


class SprintCreate(SprintBase):
    pass


class Sprint(SprintBaseInDb):
    pass


class OngoingSprint(BaseModel):
    sprint: Optional[Sprint]
