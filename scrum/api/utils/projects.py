from sqlalchemy.orm import Session

from scrum.db_models.project import Project as DBProject
from scrum.models.project import Project
from scrum.models.tag import Tag
from scrum.repositories.accessible_project import AccessibleProjectRepository


def has_access_to_project(db_session: Session, user_id: int, project_id: int) -> bool:
    accessible_repo = AccessibleProjectRepository(db_session)
    accessible_projects = accessible_repo.fetch_accessible_for_user(user_id)
    return project_id in accessible_projects


def is_project_owner(db_session: Session, user_id: int, project_id: int) -> bool:
    accessible_repo = AccessibleProjectRepository(db_session)
    accessible_projects = accessible_repo.fetch_accessible_for_user(user_id, only_owner=True)
    return project_id in accessible_projects


def project_response(project: DBProject) -> Project:
    project_dict = project.__dict__
    tags = [Tag(**tag.__dict__) for tag in project.tags]
    del project_dict['tags']
    return Project(tags=tags, **project_dict)
