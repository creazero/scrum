import datetime as dt
from typing import Optional, List

from pydantic import BaseModel


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: int
    priority: int
    weight: int


class TaskBaseInDb(TaskBase):
    id: int
    created_at: dt.datetime
    sprint_id: Optional[int]
    creator_id: int
    assignee_id: Optional[int]
    state: Optional[str]


class TaskCreate(TaskBase):
    pass


class Task(TaskBaseInDb):
    pass


class TaskBoard(BaseModel):
    todo: List[Task] = []
    in_process: List[Task] = []
    testing: List[Task] = []
    done: List[Task] = []


class TaskBoardUpdate(BaseModel):
    board: TaskBoard
    project_id: int
    sprint_id: int
