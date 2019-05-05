from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from scrum.db_models.user import User  # noqa
