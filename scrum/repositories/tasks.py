import datetime as dt
import logging
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from scrum.db_models.task import Task as DBTask, TaskState
from scrum.db_models.tag import Tag as DBTag
from scrum.models.tag import Tag
from scrum.models.task import TaskCreate, TaskBoard, Task

internal_error = HTTPException(
    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Внутренняя ошибка сервера'
)
logger = logging.getLogger(__name__)


class TaskRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def fetch_all(self) -> List[DBTask]:
        try:
            return self.session.query(DBTask).all()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise internal_error

    def fetch(self, task_id: int) -> Optional[DBTask]:
        try:
            return self.session.query(DBTask).get(task_id)
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise internal_error

    def fetch_accessible(self, accessible_projects: List[int]) -> List[DBTask]:
        try:
            return self.session.query(DBTask).\
                filter(DBTask.project_id.in_(accessible_projects)).all()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise internal_error

    def fetch_from_project(self, project_id: int) -> List[DBTask]:
        try:
            return self.session.query(DBTask).filter_by(project_id=project_id).all()
        except exc.SQLAlchemyError:
            raise internal_error

    def create(self, task_in: TaskCreate, creator_id: int) -> DBTask:
        new_task = DBTask(task_in, creator_id)
        self.session.begin()
        self.session.add(new_task)
        try:
            self.session.commit()
            self.session.refresh(new_task)
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error
        return new_task

    def delete(self, task: DBTask) -> None:
        self.session.begin()
        self.session.delete(task)
        try:
            self.session.commit()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error

    def update(self, task: DBTask, tags: List[int], **kwargs) -> DBTask:
        self.session.begin()
        for attr, value in kwargs.items():
            if attr != 'id':
                setattr(task, attr, value)
        for tag in task.tags:
            if tag.id not in tags:
                task.tags.remove(tag)
            else:
                tags.remove(tag.id)
        for tag_id in tags:
            tag: DBTag = self.session.query(DBTag).get(tag_id)
            if tag is not None:
                task.tags.append(tag)
        try:
            self.session.commit()
            self.session.refresh(task)
            return task
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error

    def update_board(self, board: TaskBoard) -> None:
        try:
            self.session.begin()
            self._update_state(board.todo, TaskState.todo)
            self._update_state(board.inProcess, TaskState.in_process)
            self._update_state(board.testing, TaskState.testing)
            self._update_state(board.done, TaskState.done)
            self.session.commit()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise internal_error

    def _update_state(self, tasks: List[Task], state: TaskState):
        for task in tasks:
            task_db: DBTask = self.fetch(task.id)
            if task_db.state != state:
                if task_db.state == TaskState.done:
                    task_db.done_date = None
                elif state == TaskState.done:
                    task_db.done_date = dt.date.today()
                task_db.state = state
