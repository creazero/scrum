from typing import List, Optional

from sqlalchemy.orm import Session

from scrum.db_models.project import Project


class ProjectRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def fetch_all(self) -> List[Project]:
        try:
            return self.session.query(Project).all()
        except Exception:
            self.session.rollback()
            raise

    def fetch(self, project_id: int) -> Optional[Project]:
        try:
            return self.session.query(Project).get(project_id)
        except Exception:
            self.session.rollback()
            raise
