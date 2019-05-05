from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import bcrypt

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, password: str, **kwargs):
        self.password = bcrypt.hash(password)
        self.username = kwargs.get('username', None)

    def __str__(self):
        return f'<User {self.id} "{self.username}"'
