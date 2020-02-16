from enum import Enum
from fastapi import FastAPI
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
