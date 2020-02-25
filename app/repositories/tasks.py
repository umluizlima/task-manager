from typing import Dict
from uuid import UUID, uuid4

from ..schemas import Task


def get_by_id(db: Dict, task_id: UUID):
    task = next((task for task in db["tasks"] if task["id"] == task_id), None)
    if task is None:
        raise Exception
    return task


def get_all(db: Dict):
    return db["tasks"]


def create(db: Dict, task: Dict):
    task.update({"id": uuid4()})
    db["tasks"].append(task)
    return task


def update(db: Dict, task_id: UUID, task: Dict):
    stored_task_data = get_by_id(db, task_id)
    stored_task_model = Task(**stored_task_data)
    updated_task = stored_task_model.copy(update=task)
    db["tasks"][db["tasks"].index(stored_task_data)] = updated_task.dict()
    return updated_task


def delete(db: Dict, task_id: UUID):
    db["tasks"].remove(get_by_id(db, task_id))
