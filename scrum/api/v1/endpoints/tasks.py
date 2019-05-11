import datetime as dt
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from scrum.api.utils.db import get_db
from scrum.api.utils.projects import has_access_to_project, is_project_owner
from scrum.api.utils.security import get_current_user
from scrum.api.utils.shared import validate_project
from scrum.api.utils.tasks import tasks_response, task_response
from scrum.db_models.task_state import TaskState
from scrum.db_models.user import User as DBUser
from scrum.models.task import Task, TaskCreate, TaskBoard, TaskBoardUpdate, TaskAssign
from scrum.models.users import User
from scrum.repositories.accessible_project import AccessibleProjectRepository
from scrum.repositories.sprints import SprintRepository
from scrum.repositories.tasks import TaskRepository
from scrum.repositories.users import UserRepository

router = APIRouter()


@router.get('/tasks', response_model=List[Task])
def get_tasks(
        project_id: int = None,
        *,
        session: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_user)
):
    task_repo = TaskRepository(session)
    if project_id is not None:
        validate_project(current_user.id, project_id,
                         current_user.is_superuser, session=session)
        tasks = task_repo.fetch_from_project(project_id)
    elif current_user.is_superuser:
        tasks = task_repo.fetch_all()
    else:
        accessible_repo = AccessibleProjectRepository(session)
        tasks = task_repo.fetch_accessible(accessible_repo.fetch_accessible_for_user(current_user.id))
    return tasks_response(tasks)


@router.post('/tasks', status_code=201)
def create_task(
        task_in: TaskCreate,
        *,
        session: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_user)
):
    validate_project(current_user.id, task_in.project_id, session=session,
                     check_owner=True, is_superuser=current_user.is_superuser)
    task_repo = TaskRepository(session)
    task_repo.create(task_in, current_user.id)
    return {'status': 'ok'}


@router.delete('/tasks/{task_id}')
def delete_task(
        task_id: int,
        *,
        session: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_user)
):
    task_repo = TaskRepository(session)
    task = task_repo.fetch(task_id)
    if task is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Задачи с данным id не существует'
        )
    if not current_user.is_superuser:
        if not has_access_to_project(session, current_user.id, task.project_id):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f'Текущий пользователь не имеет доступа к проекту {task.project_id}'
            )
        if not is_project_owner(session, current_user.id, task.project_id):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail='Текущий пользователь не имеет права на удаление задач в данном проекте'
            )
    task_repo.delete(task)
    return {'status': 'ok'}


@router.post('/tasks/assign', response_model=User)
def assign_user(
        data: TaskAssign,
        *,
        session: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_user)
):
    task_repo = TaskRepository(session)
    task = task_repo.fetch(data.task_id)
    if (not current_user.is_superuser and
            not has_access_to_project(session, current_user.id, task.project_id)):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f'Текущий пользователь не имеет доступа к проекту {task.project_id}'
        )
    if task is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Задачи с таким id не существует'
        )
    if data.user_id != 0:
        user_repo = UserRepository(session)
        user = user_repo.fetch(data.user_id)
        if user is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Пользователя с таким id не существует'
            )
        if (not user.is_superuser and
                not has_access_to_project(session, user.id, task.project_id)):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f'Назначаемый пользователь не имеет доступа к проекту {task.project_id}'
            )
        if not user.is_active:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Пользователь с таким id не активен'
            )
        task = task_repo.update(task, assignee_id=user.id)
        return user
    else:
        task = task_repo.update(task, assgnee_id=current_user.id)
        return current_user


@router.post('/tasks/assign_me/{task_id}', response_model=User)
def assign_me(
        task_id: int,
        *,
        session: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_user)
):
    task_repo = TaskRepository(session)
    task = task_repo.fetch(task_id)
    if task is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Задачи с таким id не существует'
        )
    if (not current_user.is_superuser and
            not has_access_to_project(session, current_user.id, task.project_id)):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f'Текущий пользователь не имеет доступа к проекту {task.project_id}'
        )
    task = task_repo.update(task, assignee_id=current_user.id)
    return current_user


@router.get('/tasks/board', response_model=TaskBoard)
def get_task_board(
        sprint_id: int,
        *,
        session: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_user)
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
        task.creator = session.query(DBUser).get(task.creator_id)
        if task.state == TaskState.todo:
            task_board.todo.append(task)
        elif task.state == TaskState.in_process:
            task_board.inProcess.append(task)
        elif task.state == TaskState.testing:
            task_board.testing.append(task)
        elif task.state == TaskState.done:
            task_board.done.append(task)
    return task_board


@router.put('/tasks/board')
def update_task_board(
        task_board: TaskBoardUpdate,
        *,
        session: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_user)
):
    validate_project(current_user.id, task_board.project_id,
                     current_user.is_superuser, session=session)
    sprint_repo = SprintRepository(session)
    sprint = sprint_repo.fetch(task_board.sprint_id)
    if sprint is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Спринта с данным id не существует'
        )
    if sprint.project_id != task_board.project_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Спринт с id={task_board.sprint_id} отсутствует в проекте {task_board.project_id}'
        )
    today = dt.date.today()
    if today < sprint.start_date or today > sprint.end_date:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Спринт с id={task_board.sprint_id} не является активным'
        )
    cols = [task_board.board.todo, task_board.board.inProcess,
            task_board.board.testing, task_board.board.done]
    tasks = [nested_task for sublist in cols for nested_task in sublist]
    task_repo = TaskRepository(session)
    for task in tasks:
        task_db = task_repo.fetch(task.id)
        if task_db is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'Задачи с id={task.id} не существует'
            )
        if task.project_id != task_board.project_id or task.sprint_id != task_board.sprint_id:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'Задача с id={task.id} не содержится в данном спринте'
            )
    task_repo.update_board(task_board.board)
    return {'status': 'ok'}


@router.get('/tasks/{task_id}', response_model=Task)
def get_task(
        task_id: int,
        *,
        session: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_user)
):
    task_repo = TaskRepository(session)
    task = task_repo.fetch(task_id)
    if (not current_user.is_superuser and
            not has_access_to_project(session, current_user.id, task.project_id)):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f'Текущий пользователь не имеет доступа к проекту {task.project_id}'
        )
    if task is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Задачи с таким id не найдено'
        )
    return task_response(task)


@router.put('/tasks/{task_id}', response_model=Task)
def update_task(
        task_id: int,
        task_in: TaskCreate,
        *,
        session: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_user)
):
    task_repo = TaskRepository(session)
    task = task_repo.fetch(task_id)
    if task is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Задачи с данным id не существует'
        )
    if not current_user.is_superuser:
        if not has_access_to_project(session, current_user.id, task.project_id):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f'Текущий пользователь не имеет доступа к проекту {task.project_id}'
            )
        if not is_project_owner(session, current_user.id, task.project_id):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail='Текущий пользователь не имеет права на изменение задач в данном проекте'
            )
    task = task_repo.update(task, description=task_in.description,
                            name=task_in.name, weight=task_in.weight,
                            priority=task_in.priority)
    return task_response(task)
