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
    color = Column(String)
    created_at = Column(DateTime, default=dt.datetime.utcnow())
    users: List[AccessibleProject] = relationship('AccessibleProject')
    sprint_length = Column(Integer, nullable=False, default=2)
    tags = relationship('Tag')

    def __init__(self, creator_id: int, **kwargs):
        super().__init__(**kwargs)
        ap = AccessibleProject(user_id=creator_id, role=Roles.owner)
        self.users.append(ap)
