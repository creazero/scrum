from sqlalchemy.orm import Session

from scrum.repositories.accessible_project import AccessibleProjectRepository


def has_access_to_project(db_session: Session, user_id: int, project_id: int) -> bool:
    accessible_repo = AccessibleProjectRepository(db_session)
    accessible_projects = accessible_repo.fetch_accessible_for_user(user_id)
    return project_id in accessible_projects
