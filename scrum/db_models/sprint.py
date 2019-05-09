import datetime as dt

from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from scrum.db.base_class import Base


class Sprint(Base):
    __tablename__ = 'sprints'

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), index=True, nullable=False)
    tasks = relationship('Task')

    def __init__(self, *, length: int, start_date: dt.date = None, project_id: int = None, **kwargs):
        super().__init__(**kwargs)
        self.start_date = start_date
        self.end_date = start_date + dt.timedelta(weeks=length)
        self.project_id = project_id
