import datetime as dt
import enum

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum

from scrum.db.base_class import Base


class TaskState(enum.Enum):
    todo = 'todo'
    in_process = 'in_process'
    testing = 'testing'
    done = 'done'


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(140), nullable=False)
    description = Column(String(10000), nullable=True)
    created_at = Column(DateTime, nullable=False, default=dt.datetime.utcnow)
    project_id = Column(Integer, ForeignKey('projects.id'), index=True)
    sprint_id = Column(Integer, ForeignKey('sprints.id'), index=True, nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    assignee_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    weight = Column(Integer)
    priority = Column(Integer, nullable=False, default=0)
    state = Column(Enum(TaskState))
