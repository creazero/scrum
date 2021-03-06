from typing import List

from scrum.db_models.task import Task as DBTask
from scrum.models.tag import Tag
from scrum.models.task import Task
from scrum.models.users import User


def task_response(db_task: DBTask) -> Task:
    creator = User(**db_task.creator.__dict__)
    assignee = User(**db_task.assignee.__dict__) if db_task.assignee is not None else None
    tags = [Tag(**tag.__dict__) for tag in db_task.tags]
    task_dict = db_task.__dict__
    del task_dict['creator']
    del task_dict['tags']
    del task_dict['assignee']
    return Task(assignee=assignee, creator=creator, tags=tags, **task_dict)


def tasks_response(db_tasks: List[DBTask]) -> List[Task]:
    return [task_response(task) for task in db_tasks]
