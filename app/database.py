from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db = {
    "tasks": [],
}


def setup_db():
    SQLALCHEMY_DATABASE_URL = getenv(
        "DATABASE_URL", default="postgresql://postgres:postgres@localhost/task-manager",
    )

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


Base = declarative_base()


def get_db():
    if not getenv("PERSISTENCE_ENABLED", default=False):
        yield db
    SessionLocal = setup_db()
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
