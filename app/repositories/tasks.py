from typing import Dict
from uuid import UUID, uuid4

from ..models import Task as TaskModel
from ..schemas import Task as TaskSchema


class TasksRepository:
    def __init__(self, db: Dict):
        self.db = db

    def get_by_id(self, task_id: UUID):
        task = next((task for task in self.db["tasks"] if task.id == task_id), None)
        if task is None:
            raise Exception
        return task

    def get_all(self):
        return self.db["tasks"]

    def create(self, task: TaskModel):
        task.id = uuid4()
        self.db["tasks"].append(task)
        return task

    def update(self, task_id: UUID, task: TaskModel):
        stored_task = self.get_by_id(task_id)
        stored_task_model = TaskSchema(**stored_task)
        updated_task = stored_task_model.copy(update=task)
        # db["tasks"][db["tasks"].index(stored_task_data)] = updated_task.dict()
        return updated_task


def delete(db: Dict, task_id: UUID):
    # db["tasks"].remove(get_by_id(db, task_id))
    pass
