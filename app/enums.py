from enum import Enum


class TaskStatus(str, Enum):
    TODO = "TODO"
    DONE = "DONE"
