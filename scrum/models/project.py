import datetime as dt
from typing import Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str = ''
    description: Optional[str] = None
    color: Optional[str] = None


class ProjectBaseInDb(ProjectBase):
    id: int
    created_at: dt.datetime


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBaseInDb):
    pass
