import datetime as dt
from typing import List

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from scrum.db.base_class import Base
from scrum.db_models.accessible_project import AccessibleProject, Roles


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(2000))
    color = Column(String, default='#3F51B5')
    created_at = Column(DateTime, default=dt.datetime.utcnow())
    users: List[AccessibleProject] = relationship('AccessibleProject', cascade='save-update, delete')
    sprint_length = Column(Integer, nullable=False, default=2)
    tags = relationship('Tag', cascade='save-update, delete')
    tasks = relationship('Task', cascade='save-update, delete')
    sprints = relationship('Sprint', cascade='save-update, delete')

    def __init__(self, creator_id: int, **kwargs):
        super().__init__(**kwargs)
        ap = AccessibleProject(user_id=creator_id, role=Roles.owner)
        self.users.append(ap)
