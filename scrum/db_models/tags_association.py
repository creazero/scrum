from sqlalchemy import Table, Column, Integer, ForeignKey

from scrum.db.base_class import Base

tags_association = Table('tags_association', Base.metadata,
                         Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
                         Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True))
