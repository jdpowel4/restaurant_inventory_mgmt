from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from inventory_app.shared.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def with_session(func):

    def wrapper(*args, **kwargs):

        session = SessionLocal()

        try:
            result = func(session, *args, **kwargs)
            session.commit()
            return result
        
        except:
            session.rollback()
            raise

        finally:
            session.close()
    
    return wrapper

@contextmanager
def session_scope(session: Session | None = None):

    session = SessionLocal()

    try:
        yield session
        session.commit()
    
    except:
        session.rollback()
        raise

    finally:
        session.close()