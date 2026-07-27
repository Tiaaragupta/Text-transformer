"""
Database engine + session management (Flask version).

Sprint 3 goal: "Session Management" -> connection pooling, sessions,
transactions, and safe rollback on error, all handled in one place so
every route uses the same pattern.
"""

from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine

# SQLite file lives at the project root. For PostgreSQL, swap this line for:
#   DATABASE_URL = "postgresql://user:password@localhost:5432/skypoint"
DATABASE_URL = "sqlite:///./skypoint.db"

# check_same_thread=False is required for SQLite when used with a
# multi-threaded server like Flask's dev server.
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def init_db() -> None:
    """Create tables from SQLModel metadata if they don't already exist."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    """Yields a DB session, and safely rolls back on error.

    Use it in a Flask route like:

        with get_session() as session:
            session.add(record)
            session.commit()
    """
    session = Session(engine)
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()