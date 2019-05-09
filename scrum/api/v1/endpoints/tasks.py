from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from scrum.api.utils.db import get_db
from scrum.api.utils.projects import has_access_to_project, is_project_owner
from scrum.api.utils.security import get_current_user
from scrum.db_models.task import TaskState
from scrum.db_models.user import User
from scrum.models.task import Task, TaskCreate, TaskBoard
from scrum.repositories.accessible_project import AccessibleProjectRepository
from scrum.repositories.projects import ProjectRepository
from scrum.repositories.sprints import SprintRepository
from scrum.repositories.tasks import TaskRepository

router = APIRouter()


@router.get('/tasks', response_model=List[Task])
def get_tasks(
        project_id: int = None,
        *,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    task_repo = TaskRepository(session)
    if project_id is not None:
        project_repo = ProjectRepository(session)
        if project_repo.fetch(project_id) is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Проекта с данным id не существует'
            )
        if not has_access_to_project(session, current_user.id, project_id):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f'Текущий пользователь не имеет доступа к проекту {project_id}'
            )
        return task_repo.fetch_from_project(project_id)
    elif current_user.is_superuser:
        return task_repo.fetch_all()
    else:
        accessible_repo = AccessibleProjectRepository(session)
        return task_repo.fetch_accessible(accessible_repo.fetch_accessible_for_user(current_user.id))


@router.post('/tasks', response_model=Task, status_code=201)
def create_task(
        task_in: TaskCreate,
        *,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    project_repo = ProjectRepository(session)
    if project_repo.fetch(task_in.project_id) is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Проекта с данным id не существует'
        )
    if not has_access_to_project(session, current_user.id, task_in.project_id):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f'Текущий пользователь не имеет доступа к проекту {task_in.project_id}'
        )
    if (not current_user.is_superuser and
            not is_project_owner(session, current_user.id, task_in.project_id)):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='Текущий пользователь не имеет права на создание задач в данном проекте'
        )
    task_repo = TaskRepository(session)
    return task_repo.create(task_in, current_user.id)


@router.get('/tasks/board', response_model=TaskBoard)
def get_task_board(
        sprint_id: int,
        *,
        session: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    sprint_repo = SprintRepository(session)
    sprint = sprint_repo.fetch(sprint_id)
    if sprint is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Спринта с данным id не существует'
        )
    if not has_access_to_project(session, current_user.id, sprint.project_id):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f'Текущий пользователь не имеет доступа к проекту {sprint.project_id}'
        )
    task_board = TaskBoard()
    for task in sprint.tasks:
        if task.state == TaskState.todo:
            task_board.todo.append(task)
        elif task.state == TaskState.in_process:
            task_board.in_process.append(task)
        elif task.state == TaskState.testing:
            task_board.testing.append(task)
        elif task.state == TaskState.done:
            task_board.done.append(task)
    return task_board
