from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import os

engine = create_engine(os.getenv('DATABASE_URL', 'postgresql://localhost/subscriptions'))
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def db_session():
    session = scoped_session(SessionLocal)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()