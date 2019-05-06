from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from scrum.db_models.project import Project as DBProject
from scrum.models.project import ProjectCreate
from scrum.repositories.accessible_project import AccessibleProjectRepository


class ProjectRepository(object):
    def __init__(self, session: Session):
        self.session = session
        self.accessible_project_repo = AccessibleProjectRepository(self.session)

    def fetch_all(self, user_id: int, is_superuser: bool) -> List[DBProject]:
        try:
            accessible_projects = self.accessible_project_repo.fetch_accessible_for_user(user_id)
            return self.session.query(DBProject).\
                filter(or_(DBProject.id.in_(accessible_projects), is_superuser))
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
