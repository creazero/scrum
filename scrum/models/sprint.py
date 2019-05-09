import datetime as dt

from pydantic import BaseModel


class SprintBase(BaseModel):
    start_date: dt.date
    project_id: int


class SprintBaseInDb(SprintBase):
    id: int


class SprintCreate(SprintBase):
    pass


class Sprint(SprintBaseInDb):
    end_date: dt.date
