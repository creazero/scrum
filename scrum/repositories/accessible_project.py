from typing import List

from sqlalchemy.orm import Session

from scrum.db_models.accessible_project import AccessibleProject


class AccessibleProjectRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def fetch_accessible_for_user(self, user_id: int, only_owner: bool = False) -> List[int]:
        accessible = self.session.query(AccessibleProject)\
            .filter_by(user_id=user_id)
        if only_owner:
            accessible = accessible.filter_by(role='owner')
        return [row.project_id for row in accessible.all()]
