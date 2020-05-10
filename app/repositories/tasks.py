from typing import Dict, List
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from ..models import Task


class TasksRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, task: Task):
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def find_all(self):
        return self.db.query(Task).all()

    def find_by_id(self, id: UUID):
        return self._filter_by_id(id).one()

    def delete_by_id(self, id: UUID):
        if not self._filter_by_id(id).delete():
            raise NoResultFound()
        self.db.commit()

    def create(self, data: Dict):
        return self.save(Task(**data))

    def update_by_id(self, id: UUID, data: Dict):
        if not self._filter_by_id(id).update(data):
            raise NoResultFound()
        self.db.commit()
        return self.find_by_id(id)

    def _filter_by_id(self, id: UUID):
        return self.db.query(Task).filter(Task.id == id)
