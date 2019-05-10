from typing import List

from scrum.db_models.task import Task as DBTask
from scrum.models.task import Task
from scrum.models.users import User


def tasks_response(db_tasks: List[DBTask]) -> List[Task]:
    tasks: List[Task] = []
    for task in db_tasks:
        creator = User(**task.creator.__dict__)
        task_dict = task.__dict__
        del task_dict['creator']
        task = Task(creator=creator, **task_dict)
        tasks.append(task)
    return tasks
