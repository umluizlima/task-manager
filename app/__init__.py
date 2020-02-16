from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from uuid import UUID, uuid4

TASKS = []


class TaskStatus(str, Enum):
    TODO = "TODO"
    DONE = "DONE"


class TaskInput(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(max_length=140)
    status: TaskStatus = TaskStatus.TODO


class Task(TaskInput):
    id: UUID


app = FastAPI()


@app.get("/tasks")
def list():
    return TASKS


@app.post('/tasks', response_model=Task, status_code=201)
def create(task: TaskInput):
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


def find_task_by_id(task_id):
    task = next(
        (task for task in TASKS if task["id"] == task_id),
        None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
