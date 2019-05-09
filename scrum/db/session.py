from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from scrum.core import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=True, autoflush=False, bind=engine)
