from fastapi import APIRouter, Depends, HTTPException
from operator import itemgetter
from typing import Dict, List
from uuid import UUID, uuid4

from ..database import get_db
from ..repositories import tasks
from ..schemas import Task, TaskCreate, TaskUpdate


router = APIRouter()


@router.get("/tasks", response_model=List[Task])
def list(db: Dict = Depends(get_db)):
    return sorted(
        tasks.get_all(db), key=lambda task: task["status"].value, reverse=True
    )


@router.post("/tasks", response_model=Task, status_code=201)
def create(task: TaskCreate, db: Dict = Depends(get_db)):
    new_task = task.dict()
    return tasks.create(db, new_task)


@router.delete("/tasks/{task_id}", status_code=204)
def delete(task_id: UUID, db: Dict = Depends(get_db)):
    try:
        return tasks.delete(db, task_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")


@router.get("/tasks/{task_id}", response_model=Task)
def read(task_id: UUID, db: Dict = Depends(get_db)):
    try:
        return tasks.get_by_id(db, task_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")


@router.put("/tasks/{task_id}", response_model=Task)
def update(task_id: UUID, task: TaskUpdate, db: Dict = Depends(get_db)):
    try:
        return tasks.update(db, task_id, task.dict(exclude_unset=True))
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")
