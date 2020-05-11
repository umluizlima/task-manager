from uuid import uuid4

from pytest import fixture, raises

from app.enums import TaskStatus
from app.repositories import TasksRepository


@fixture(scope="function")
def repository(db):
    return TasksRepository(db)


new_task = {
    "title": "title",
    "description": "description",
    "status": TaskStatus.TODO,
}


def test_create_should_return_created_task(repository):
    task = repository.create(new_task)
    assert task.title == new_task["title"]


def test_create_task_should_have_id(repository):
    task = repository.create(new_task)
    assert task.id


def test_create_tasks_should_be_persisted(repository):
    repository.create(new_task)
    repository.create(new_task)
    assert len(repository.find_all()) == 2


def test_find_all_should_return_list(repository):
    assert isinstance(repository.find_all(), list)


def test_find_all_should_return_existing_tasks(repository):
    task = repository.create(new_task)
    result = repository.find_all()
    assert result[0] == task


def test_find_by_id_should_return_task(repository):
    task = repository.create(new_task)
    result = repository.find_by_id(task.id)
    assert result.id == task.id


def test_find_by_id_should_raise_exception_if_not_found(repository):
    with raises(Exception):
        repository.find_by_id(uuid4())


def test_update_by_id_should_update_task(repository):
    task = repository.create(new_task)
    updated_task = repository.update_by_id(task.id, {"title": "new title"})
    assert updated_task.title == "new title"


def test_update_by_id_should_raise_exception_if_not_found(repository):
    with raises(Exception):
        repository.update_by_id(uuid4(), {})


def test_delete_by_id_should_remove_task(repository):
    task = repository.create(new_task)
    repository.delete_by_id(task.id)
    assert task not in repository.find_all()


def test_delete_by_id_should_raise_exception_if_not_found(repository):
    with raises(Exception):
        repository.delete_by_id(uuid4())
