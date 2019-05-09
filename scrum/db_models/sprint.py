from sqlalchemy import Column, Integer, Date, ForeignKey

from scrum.db.base_class import Base


class Sprint(Base):
    __tablename__ = 'sprints'

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), index=True)
