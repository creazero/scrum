import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum

from scrum.db.base_class import Base


class Roles(enum.Enum):
    owner = 'owner'
    dev = 'dev'


class AccessibleProjects(Base):
    __tablename__ = 'accessible_projects'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    role = Column(Enum(Roles))
