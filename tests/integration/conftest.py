from pytest import fixture

from app.database import get_db


@fixture(autouse=True)
def db():
    db = next(get_db())
    yield db
    db["tasks"].clear()
