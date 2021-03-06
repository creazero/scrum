import datetime as dt
from typing import Optional, List, Union

from pydantic import BaseModel

from scrum.models.task import Task


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
    tasks: List[Task] = []

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


class DataSet(BaseModel):
    data: List[Optional[Union[float, int]]]
    label: str


class ChartData(BaseModel):
    data: List[DataSet]
    labels: List[str]
