import logging
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import or_, exc
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from scrum.db_models.accessible_project import AccessibleProject
from scrum.db_models.project import Project as DBProject
from scrum.db_models.user import User as DBUser
from scrum.models.project import ProjectCreate, Project

commit_exception = HTTPException(
    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Произошла внутренняя ошибка'
)
logger = logging.getLogger(__name__)


class ProjectRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def fetch_all(self, accessible_projects: List[int], is_superuser: bool) -> List[DBProject]:
        try:
            if is_superuser:
                return self.session.query(DBProject).all()
            else:
                return self.session.query(DBProject).\
                    filter(or_(DBProject.id.in_(accessible_projects), is_superuser)).all()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise commit_exception

    def fetch(self, project_id: int) -> Optional[DBProject]:
        try:
            return self.session.query(DBProject).get(project_id)
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise commit_exception

    def check_name(self, project_name: str) -> Optional[DBProject]:
        try:
            return self.session.query(DBProject).filter_by(name=project_name).first()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            raise commit_exception

    def create(self, user_data: ProjectCreate, creator_id: int) -> DBProject:
        new_project = DBProject(creator_id, name=user_data.name,
                                description=user_data.description,
                                color=user_data.color)
        self.session.begin()
        self.session.add(new_project)
        try:
            self.session.commit()
            self.session.refresh(new_project)
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise commit_exception
        return new_project

    def delete(self, project: DBProject) -> None:
        self.session.begin()
        self.session.delete(project)
        try:
            self.session.commit()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise commit_exception

    def give_access(self, project: DBProject, user: DBUser) -> None:
        self.session.begin()
        ap = AccessibleProject(project_id=project.id, user_id=user.id, role='dev')
        project.users.append(ap)
        try:
            self.session.commit()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise commit_exception

    def update(self, project: DBProject, project_in: Project) -> DBProject:
        self.session.begin()
        project.name = project_in.name
        project.description = project.description
        project.sprint_length = project_in.sprint_length
        project.color = project_in.color
        try:
            self.session.commit()
            self.session.refresh(project)
            return project
        except exc.SQLAlchemyError as e:
            logger.error(e)
            self.session.rollback()
            raise commit_exception
