import datetime as dt
import enum
from typing import Optional, List

from pydantic import BaseModel

from scrum.models.tag import Tag


class AccessOp(enum.Enum):
    give = 'give'
    revoke = 'revoke'


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


class ProjectAccess(BaseModel):
    project_id: int
    user_id: int
    op: AccessOp

    class Config:
        allow_population_by_alias = True
        fields = {
            'project_id': 'projectId',
            'user_id': 'userId'
        }
