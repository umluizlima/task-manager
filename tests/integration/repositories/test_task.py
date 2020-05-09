from pytest import raises
from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK

from app import app
from app.enums import TaskStatus
from app.repositories import TasksRepository

new_task = {
    "title": "title",
    "description": "description",
}


def test_create_should_return_created_task(db):
    result = TasksRepository(db).create(new_task)
    assert result["title"] == new_task["title"]


def test_create_task_should_have_id(db):
    result = TasksRepository(db).create(new_task)
    assert "id" in result


def test_create_tasks_should_be_persisted(db):
    TasksRepository(db).create(new_task)
    TasksRepository(db).create(new_task)
    assert len(db["tasks"]) == 2


def test_get_all_should_return_list(db):
    result = TasksRepository(db).get_all()
    assert isinstance(result, list)


def test_get_all_should_return_existing_tasks(db):
    db["tasks"].append(new_task)
    result = TasksRepository(db).get_all()
    assert result[0] == new_task


def test_get_by_id_should_return_task(db):
    task = TasksRepository(db).create(new_task)
    result = TasksRepository(db).get_by_id(task["id"])
    assert result["id"] == task["id"]


def test_get_by_id_should_raise_exception_if_not_found(db):
    with raises(Exception):
        TasksRepository(db).get_by_id("fake-uuid")


def test_update_should_update_task(db):
    task = TasksRepository(db).create(new_task)
    updated_task = TasksRepository(db).update(task["id"], {"abc": 123})
    assert updated_task.abc == 123


def test_update_should_raise_exception_if_not_found(db):
    with raises(Exception):
        TasksRepository(db).delete("fake-uuid")


def test_delete_should_remove_task(db):
    task = TasksRepository(db).create(new_task)
    TasksRepository(db).delete(task["id"])
    assert task not in db["tasks"]


def test_delete_should_raise_exception_if_not_found(db):
    with raises(Exception):
        TasksRepository(db).delete("fake-uuid")
