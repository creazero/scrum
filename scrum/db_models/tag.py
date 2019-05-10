from sqlalchemy import Column, Integer, ForeignKey, String

from scrum.db.base_class import Base


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    color = Column(String)
