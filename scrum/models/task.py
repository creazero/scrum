import datetime as dt
from typing import Optional, List

from pydantic import BaseModel, Schema

from scrum.db_models.task_state import TaskState
from scrum.models.users import User


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
    creator: User
    assignee_id: Optional[int]
    state: Optional[TaskState] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBaseInDb):

    class Config:
        allow_population_by_alias = True
        fields = {
            'project_id': 'projectId',
            'sprint_id': 'sprintId',
            'assignee_id': 'assigneeId',
            'created_at': 'createdAt',
            'creator_id': 'creatorId'
        }


class TaskBoard(BaseModel):
    todo: List[Task] = []
    inProcess: List[Task] = []
    testing: List[Task] = []
    done: List[Task] = []


class TaskBoardUpdate(BaseModel):
    board: TaskBoard
    project_id: int
    sprint_id: int
