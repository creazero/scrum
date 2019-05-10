import datetime as dt
from typing import Optional, List

from pydantic import BaseModel

from scrum.db_models.task_state import TaskState
from scrum.models.users import User


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    projectId: int
    priority: int
    weight: int


class TaskBaseInDb(TaskBase):
    id: int
    createdAt: dt.datetime
    sprintId: Optional[int]
    creatorId: int
    creator: User
    assigneeId: Optional[int]
    state: Optional[TaskState] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBaseInDb):
    pass


class TaskBoard(BaseModel):
    todo: List[Task] = []
    inProcess: List[Task] = []
    testing: List[Task] = []
    done: List[Task] = []


class TaskBoardUpdate(BaseModel):
    board: TaskBoard
    project_id: int
    sprint_id: int
