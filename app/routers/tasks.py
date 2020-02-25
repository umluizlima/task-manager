from fastapi import APIRouter, Depends, HTTPException
from operator import itemgetter
from typing import List
from uuid import UUID, uuid4

from ..database import get_db
from ..schemas import Task, TaskCreate, TaskUpdate


router = APIRouter()


@router.get("/tasks", response_model=List[Task])
def list(TASKS: List = Depends(get_db)):
    return sorted(TASKS, key=lambda task: task["status"].value, reverse=True)


@router.post("/tasks", response_model=Task, status_code=201)
def create(task: TaskCreate, TASKS: List = Depends(get_db)):
    new_task = task.dict()
    new_task.update({"id": uuid4()})
    TASKS.append(new_task)
    return new_task


@router.delete("/tasks/{task_id}", status_code=204)
def delete(task_id: UUID, TASKS: List = Depends(get_db)):
    return TASKS.remove(find_task_by_id(TASKS, task_id))


@router.get("/tasks/{task_id}", response_model=Task)
def read(task_id: UUID, TASKS: List = Depends(get_db)):
    return find_task_by_id(TASKS, task_id)


@router.put("/tasks/{task_id}", response_model=Task)
def update(task_id: UUID, task: TaskUpdate, TASKS: List = Depends(get_db)):
    stored_task_data = find_task_by_id(TASKS, task_id)
    stored_task_model = Task(**stored_task_data)
    update_data = task.dict(exclude_unset=True)
    updated_task = stored_task_model.copy(update=update_data)
    TASKS[TASKS.index(stored_task_data)] = updated_task.dict()

    return updated_task


def find_task_by_id(tasks, task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
