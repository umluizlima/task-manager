from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db = {
    "tasks": [],
}


def get_url():
    return getenv(
        "DATABASE_URL", default="postgresql://postgres:postgres@localhost/task-manager",
    )


engine = create_engine(get_url())
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    if getenv("PERSISTENCE_ENABLED", default=False):
        try:
            session = Session()
            yield session
            session.commit()
        except Exception as error:
            session.rollback()
            raise error
        finally:
            session.close()
    else:
        yield db
