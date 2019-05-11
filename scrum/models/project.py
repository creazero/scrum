import datetime as dt
from typing import Optional, List

from pydantic import BaseModel

from scrum.models.tag import Tag


class ProjectBase(BaseModel):
    name: str = ''
    description: Optional[str] = None
    color: Optional[str] = None
    sprint_length: int

    class Config:
        allow_population_by_alias = True
        fields = {
            'sprint_length': 'sprintLength'
        }


class ProjectBaseInDb(ProjectBase):
    id: int
    created_at: dt.datetime
    tags: List[Tag] = []

    class Config:
        allow_population_by_alias = True
        fields = {
            'created_at': 'createdAt'
        }


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBaseInDb):
    pass
