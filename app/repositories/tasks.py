from typing import Dict
from uuid import UUID, uuid4

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from .. import models


class TasksRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, task: Dict):
        db_task = models.Task(**task)
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task

    def get_all(self):
        return self.session.query(models.Task).all()

    def get_by_id(self, id: UUID):
        return self._filter_by_id_query(id).one()

    def update(self, id: UUID, task: Dict):
        updated_rows = self._filter_by_id_query(id).update(task)
        if updated_rows == 0:
            raise NoResultFound()
        self.session.commit()
        return self.get_by_id(id)

    def delete(self, id: UUID):
        deleted_rows = self._filter_by_id_query(id).delete()
        if deleted_rows == 0:
            raise NoResultFound()
        self.session.commit()

    def _filter_by_id_query(self, id: UUID):
        return self.session.query(models.Task).filter(models.Task.id == id)
