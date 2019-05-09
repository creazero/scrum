from typing import List

from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from scrum.db_models.sprint import Sprint as DBSprint
from scrum.models.sprint import SprintCreate

internal_error = HTTPException(
    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Внутренняя ошибка сервера'
)


class SprintRepository(object):
    def __init__(self, session: Session):
        self.session = session

    def fetch_all(self, accessible_projects: List[int]) -> List[DBSprint]:
        try:
            return self.session.query(DBSprint).\
                filter(DBSprint.project_id.in_(accessible_projects)).all()
        except exc.SQLAlchemyError:
            self.session.rollback()
            raise internal_error

    def create(self, sprint_in: SprintCreate, sprint_length: int = 2) -> DBSprint:
        sprint = DBSprint(length=sprint_length, start_date=sprint_in.start_date)
        self.session.add(sprint)
        try:
            self.session.commit()
            self.session.refresh(sprint)
        except exc.SQLAlchemyError:
            self.session.rollback()
            raise internal_error
        return sprint
