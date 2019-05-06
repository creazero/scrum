from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from scrum.db_models.project import Project as DBProject
from scrum.models.project import ProjectCreate


class ProjectRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def fetch_all(self) -> List[DBProject]:
        try:
            return self.session.query(DBProject).all()
        except Exception:
            self.session.rollback()
            raise

    def fetch(self, project_id: int) -> Optional[DBProject]:
        try:
            return self.session.query(DBProject).get(project_id)
        except Exception:
            self.session.rollback()
            raise

    def create(self, user_data: ProjectCreate, creator_id: int) -> DBProject:
        try:
            new_project = DBProject(creator_id, name=user_data.name,
                                    description=user_data.description,
                                    color=user_data.color)
            self.session.add(new_project)
            self.session.commit()
            self.session.refresh(new_project)
            return new_project
        except Exception:
            self.session.rollback()
            raise

    def delete(self, project_id: int) -> None:
        project = self.fetch(project_id)
        if project is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail='Проект с таким id не найден'
            )
        self.session.delete(project)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Произошла ошибка при удалении проекта'
            )
