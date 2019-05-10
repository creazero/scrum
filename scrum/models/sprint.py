import datetime as dt
from typing import Optional, List

from pydantic import BaseModel


class SprintBase(BaseModel):
    start_date: dt.date
    project_id: int


class SprintBaseInDb(SprintBase):
    id: int
    end_date: dt.date


class SprintCreate(SprintBase):
    tasks: List[int] = []

    class Config:
        allow_population_by_alias = True
        fields = {
            'start_date': 'startDate',
            'project_id': 'projectId',
        }


class Sprint(SprintBaseInDb):

    class Config:
        allow_population_by_alias = True
        fields = {
            'start_date': 'startDate',
            'end_date': 'endDate',
            'project_id': 'projectId',
        }


class OngoingSprint(BaseModel):
    sprint: Optional[Sprint]


class IntersectionCheck(BaseModel):
    start_date: dt.date
    project_id: int

    class Config:
        allow_population_by_alias = True
        fields = {
            'start_date': 'startDate',
            'project_id': 'projectId',
        }

