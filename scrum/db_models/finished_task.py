import datetime as dt

from sqlalchemy import Column, Date, Integer, ForeignKey

from scrum.db.base_class import Base


class FinishedTask(Base):
    __tablename__ = 'finished_tasks'

    finish_date = Column(Date, default=dt.date.today)
    task_id = Column(Integer, ForeignKey('tasks.id'), index=True)
    sprint_id = Column(Integer, ForeignKey('sprints.id'), primary_key=True)
