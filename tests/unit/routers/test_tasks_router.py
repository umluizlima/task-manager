from unittest.mock import MagicMock
from uuid import uuid4

from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app import app
from app.database import get_db
from app.enums import TaskStatus
from app.models import Task
from app.repositories.tasks import TasksRepository


def mock_get_db():
    return MagicMock()


app.dependency_overrides[get_db] = mock_get_db

todo_dict = {
    "title": "Todo",
    "description": "Todo",
    "status": TaskStatus.TODO,
}
todo_task = Task(id=uuid4(), **todo_dict)

done_dict = {
    "title": "Done",
    "description": "Done",
    "status": TaskStatus.DONE,
}
done_task = Task(id=uuid4(), **done_dict)


@fixture(scope="function")
def list_response(client):
    TasksRepository.find_all = MagicMock(return_value=[done_task, todo_task])
    yield client.get("/tasks")
    TasksRepository.find_all.assert_called_once()


def test_list_should_return_status_200(list_response):
    assert list_response.status_code == HTTP_200_OK


def test_list_should_return_json(list_response):
    assert list_response.headers["Content-Type"] == "application/json"


def test_list_should_return_list(list_response):
    assert isinstance(list_response.json(), list)


def test_listed_task_should_have_id(list_response):
    assert "id" in list_response.json().pop()


def test_listed_task_should_have_title(list_response):
    assert "title" in list_response.json().pop()


def test_listed_task_should_have_description(list_response):
    assert "description" in list_response.json().pop()


def test_listed_task_should_have_status(list_response):
    assert "status" in list_response.json().pop()


def test_listed_tasks_should_be_ordered_by_status(list_response):
    assert list_response.json()[0]["status"] == "TODO"


@fixture(scope="function")
def read_response(client):
    TasksRepository.find_by_id = MagicMock(return_value=done_task)
    yield client.get(f"/tasks/{done_task.id}")
    TasksRepository.find_by_id.assert_called_once_with(done_task.id)


def test_read_endpoint_should_accept_get(read_response):
    assert read_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_read_should_return_status_200_if_task_found(read_response):
    assert read_response.status_code == HTTP_200_OK


def test_read_task_should_return_task_if_found(read_response):
    response_task = Task(**read_response.json())
    assert response_task.id == str(done_task.id)
    assert response_task.title == done_task.title
    assert response_task.description == done_task.description
    assert response_task.status == done_task.status


def test_read_should_return_status_404_if_task_not_found(client):
    TasksRepository.find_by_id = MagicMock(side_effect=Exception)
    response = client.get(f"/tasks/{done_task.id}")
    assert response.status_code == HTTP_404_NOT_FOUND
    TasksRepository.find_by_id.assert_called_once_with(done_task.id)


@fixture(scope="function")
def create_response(client):
    TasksRepository.create = MagicMock(return_value=todo_task)
    yield client.post("/tasks", json=todo_dict)
    TasksRepository.create.assert_called_once_with(todo_dict)


def test_task_endpoint_should_accept_post(create_response):
    assert create_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_task_should_have_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_task_title_should_have_at_least_3_characters(client):
    response = client.post("/tasks", json={"title": 2 * "*"})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_task_title_should_have_at_most_50_characters(client):
    response = client.post("/tasks", json={"title": 51 * "*"})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_task_should_have_description(client):
    response = client.post("/tasks", json={"title": "Title"})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_task_description_should_have_at_most_140_characters(client):
    response = client.post("/tasks", json={"title": "Title", "description": "*" * 141})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_created_task_should_be_returned(create_response):
    assert create_response.json()["title"] == todo_dict["title"]
    assert create_response.json()["description"] == todo_dict["description"]


def test_created_task_should_return_status_201(create_response):
    assert create_response.status_code == HTTP_201_CREATED


@fixture(scope="function")
def delete_response(client):
    TasksRepository.delete_by_id = MagicMock()
    yield client.delete(f"/tasks/{todo_task.id}")
    TasksRepository.delete_by_id.assert_called_once_with(todo_task.id)


def test_delete_task_endpoint_should_accept_delete(delete_response):
    assert delete_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_delete_task_should_return_status_204(delete_response):
    assert delete_response.status_code == HTTP_204_NO_CONTENT


def test_delete_task_should_return_status_404_if_task_not_found(client):
    TasksRepository.delete_by_id = MagicMock(side_effect=Exception)
    response = client.delete(f"/tasks/{todo_task.id}")
    assert response.status_code == HTTP_404_NOT_FOUND
    TasksRepository.delete_by_id.assert_called_once_with(todo_task.id)


@fixture(scope="function")
def update_response(client):
    TasksRepository.update_by_id = MagicMock(return_value=todo_task)
    yield client.put(f"/tasks/{todo_task.id}", json=todo_dict)
    TasksRepository.update_by_id.assert_called_once_with(todo_task.id, todo_dict)


def test_update_task_endpoint_should_accept_put(update_response):
    assert update_response.status_code != HTTP_405_METHOD_NOT_ALLOWED


def test_update_task_should_return_status_404_if_task_not_found(client):
    TasksRepository.update_by_id = MagicMock(side_effect=Exception)
    response = client.put(f"/tasks/{todo_task.id}", json=todo_dict)
    assert response.status_code == HTTP_404_NOT_FOUND
    TasksRepository.update_by_id.assert_called_once_with(todo_task.id, todo_dict)


def test_update_task_should_not_have_required_fields(client):
    response = client.put(f"/tasks/{todo_task.id}", json={})
    assert response.status_code != HTTP_422_UNPROCESSABLE_ENTITY


def test_update_task_should_return_updated_task(update_response):
    assert update_response.json()["title"] == todo_dict["title"]


def test_update_task_should_ignore_unknown_fields(client):
    update_data = {"key": "value", **todo_dict}
    TasksRepository.update_by_id = MagicMock(return_value=todo_task)
    client.put(f"/tasks/{todo_task.id}", json=update_data)
    TasksRepository.update_by_id.assert_called_once_with(todo_task.id, todo_dict)


def test_update_task_should_return_status_200_if_successful(update_response):
    assert update_response.status_code == HTTP_200_OK
