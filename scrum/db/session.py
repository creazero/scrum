from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class SessionScope(object):
    def __init__(self, db_url: str):
        super().__init__()
        self._engine = create_engine(db_url)
        self._session_provider = scoped_session(sessionmaker(self._engine))

    @contextmanager
    def __call__(self, commit_on_exit=True, *args, **kwargs):
        session = self._session_provider()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        else:
            if commit_on_exit:
                session.commit()
        finally:
            session.close()
