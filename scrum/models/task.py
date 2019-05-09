import datetime as dt
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: int
    priority: int


class TaskBaseInDb(TaskBase):
    id: int
    created_at: dt.datetime
    sprint_id: Optional[int]
    creator_id: int
    assignee_id: Optional[int]
    weight: int
    state: Optional[str]


class TaskCreate(TaskBase):
    pass


class Task(TaskBaseInDb):
    pass
