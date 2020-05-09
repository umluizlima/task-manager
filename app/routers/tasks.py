from fastapi import APIRouter, Depends, HTTPException
from operator import itemgetter
from typing import Dict, List
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from ..database import get_db
from ..repositories.tasks import TasksRepository
from ..schemas import Task, TaskCreate, TaskUpdate


router = APIRouter()


@router.get("/tasks", response_model=List[Task])
def list(db: Session = Depends(get_db)):
    return sorted(
        TasksRepository(db).get_all(), key=lambda task: task.status.value, reverse=True
    )


@router.post("/tasks", response_model=Task, status_code=201)
def create(task: TaskCreate, db: Session = Depends(get_db)):
    return TasksRepository(db).create(task.dict())


@router.delete("/tasks/{task_id}", status_code=204)
def delete(task_id: UUID, db: Session = Depends(get_db)):
    try:
        return TasksRepository(db).delete(task_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")


@router.get("/tasks/{task_id}", response_model=Task)
def read(task_id: UUID, db: Session = Depends(get_db)):
    try:
        return TasksRepository(db).get_by_id(task_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")


@router.put("/tasks/{task_id}", response_model=Task)
def update(task_id: UUID, task: TaskUpdate, db: Session = Depends(get_db)):
    try:
        return TasksRepository(db).update(task_id, task.dict(exclude_unset=True))
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")
