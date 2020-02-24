from pydantic import BaseModel, constr
from typing import List
from uuid import UUID, uuid4

from .enums import TaskStatus


class TaskBase(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(max_length=140)
    status: TaskStatus = TaskStatus.TODO


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: constr(min_length=3, max_length=50) = None
    description: constr(max_length=140) = None
    status: TaskStatus = None


class Task(TaskBase):
    id: UUID
