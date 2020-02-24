from fastapi import FastAPI, HTTPException
from operator import itemgetter
from pydantic import BaseModel, constr
from typing import List
from uuid import UUID, uuid4

from .database import TASKS
from .enums import TaskStatus
from .schemas import Task, TaskCreate, TaskUpdate

app = FastAPI()


@app.get("/tasks", response_model=List[Task])
def list():
    return sorted(TASKS, key=lambda task: task["status"].value, reverse=True)


@app.post("/tasks", response_model=Task, status_code=201)
def create(task: TaskCreate):
    new_task = task.dict()
    new_task.update({"id": uuid4()})
    TASKS.append(new_task)
    return new_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete(task_id: UUID):
    return TASKS.remove(find_task_by_id(task_id))


@app.get("/tasks/{task_id}", response_model=Task)
def read(task_id: UUID):
    return find_task_by_id(task_id)


@app.put("/tasks/{task_id}", response_model=Task)
def update(task_id: UUID, task: TaskUpdate):
    stored_task_data = find_task_by_id(task_id)
    stored_task_model = Task(**stored_task_data)
    update_data = task.dict(exclude_unset=True)
    updated_task = stored_task_model.copy(update=update_data)
    TASKS[TASKS.index(stored_task_data)] = updated_task.dict()

    return updated_task


def find_task_by_id(task_id):
    task = next((task for task in TASKS if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
