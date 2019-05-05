import datetime as dt

from sqlalchemy import Column, Integer, String, DateTime

from scrum.db.base_class import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(2000))
    color = Column(String)
    created_at = Column(DateTime, default=dt.datetime.utcnow())
