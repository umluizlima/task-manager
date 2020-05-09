from os import environ
from subprocess import run
from unittest.mock import MagicMock
from uuid import uuid4

from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK
from testcontainers.postgres import PostgresContainer

from app import app
from app.database import get_db
from app.enums import TaskStatus
from app.models import Task
from app.repositories.tasks import TasksRepository


client = TestClient(app)


def mock_get_db():
    return MagicMock()


app.dependency_overrides[get_db] = mock_get_db


todo_task = Task(id=uuid4(), title="Todo", description="Todo", status=TaskStatus.TODO)
done_task = Task(id=uuid4(), title="Done", description="Done", status=TaskStatus.DONE)


@fixture(scope="function")
def list_response():
    TasksRepository.get_all = MagicMock(return_value=[done_task, todo_task])
    yield client.get("/tasks")
    TasksRepository.get_all.assert_called_once()


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
def read_response():
    TasksRepository.get_by_id = MagicMock(return_value=done_task)
    yield client.get(f"/tasks/{done_task.id}")
    TasksRepository.get_by_id.assert_called_once_with(done_task.id)


def test_read_endpoint_should_accept_get(read_response):
    assert read_response.status_code != 405


def test_read_should_return_status_200_if_task_found(read_response):
    assert read_response.status_code == 200


def test_read_task_should_return_task_if_found(read_response):
    response_task = Task(**read_response.json())
    assert response_task.id == str(done_task.id)
    assert response_task.title == done_task.title
    assert response_task.description == done_task.description
    assert response_task.status == done_task.status


def test_read_should_return_status_404_if_task_not_found():
    TasksRepository.get_by_id = MagicMock(side_effect=Exception)
    response = client.get(f"/tasks/{done_task.id}")
    assert response.status_code == 404
    TasksRepository.get_by_id.assert_called_once_with(done_task.id)


# def test_task_endpoint_should_accept_post():
#     response = client.post("/tasks")
#     assert response.status_code != 405


# def test_task_should_have_title():
#     response = client.post("/tasks", json={})
#     assert response.status_code == 422


# def test_task_title_should_have_at_least_3_characters():
#     response = client.post("/tasks", json={"title": 2 * "*"})
#     assert response.status_code == 422


# def test_task_title_should_have_at_most_50_characters():
#     response = client.post("/tasks", json={"title": 51 * "*"})
#     assert response.status_code == 422


# def test_task_should_have_description():
#     response = client.post("/tasks", json={"title": "Title"})
#     assert response.status_code == 422


# def test_task_description_should_have_at_most_140_characters():
#     response = client.post("/tasks", json={"title": "Title", "description": "*" * 141})
#     assert response.status_code == 422


# def test_created_task_should_be_returned():
#     task = {"title": "Title", "description": "Description"}
#     response = client.post("/tasks", json=task)
#     assert response.json()["title"] == task["title"]
#     assert response.json()["description"] == task["description"]


# def test_created_task_should_have_unique_id():
#     task1 = {"title": "Title 1", "description": "Description1"}
#     task2 = {"title": "Title 2", "description": "Description2"}
#     response1 = client.post("/tasks", json=task1)
#     response2 = client.post("/tasks", json=task2)
#     assert response1.json()["id"] != response2.json()["id"]


# def test_created_task_should_have_default_status_todo():
#     task = {"title": "Title", "description": "Description"}
#     response = client.post("/tasks", json=task)
#     assert response.json()["status"] == "TODO"


# def test_created_task_should_return_status_201():
#     task = {"title": "Title", "description": "Description"}
#     response = client.post("/tasks", json=task)
#     assert response.status_code == 201


# # def test_created_task_should_be_persisted(tasks):
# #     task = {"title": "Title", "description": "Description"}
# #     response = client.post("/tasks", json=task)
# #     assert response.status_code == 201
# #     assert len(tasks) == 1


# def test_delete_task_endpoint_should_accept_delete():
#     response = client.delete("/tasks/task_id")
#     assert response.status_code != 405


# def test_delete_task_should_return_status_204():
#     task = {"title": "Title", "description": "Description"}
#     created_task = client.post("/tasks", json=task).json()
#     response = client.delete(f'/tasks/{created_task["id"]}')
#     assert response.status_code == 204


# def test_delete_task_should_return_status_404_if_task_not_found():
#     response = client.delete("/tasks/8415b9a1-cca3-40c2-af7b-1ad689889fba")
#     assert response.status_code == 404


# # def test_delete_task_should_remove_task_from_persistence(tasks):
# #     task = {"title": "Title", "description": "Description"}
# #     created_task = client.post("/tasks", json=task).json()
# #     client.delete(f'/tasks/{created_task["id"]}')
# #     assert len(tasks) == 0


# def test_update_task_endpoint_should_accept_put():
#     response = client.put("/tasks/task_id")
#     assert response.status_code != 405


# def test_update_task_should_return_status_404_if_task_not_found():
#     task = {"title": "Title", "description": "Description"}
#     response = client.put("/tasks/8415b9a1-cca3-40c2-af7b-1ad689889fba", json=task)
#     assert response.status_code == 404


# def test_update_task_should_not_have_required_fields():
#     task = {"title": "Title", "description": "Description"}
#     created_task = client.post("/tasks", json=task).json()

#     update_fields = {}
#     response = client.put(f'/tasks/{created_task["id"]}', json=update_fields)
#     assert response.status_code != 422


# def test_update_task_should_return_updated_task():
#     task = {"title": "Title", "description": "Description"}
#     created_task = client.post("/tasks", json=task).json()

#     update_fields = {"title": "New title"}
#     updated_task = client.put(f'/tasks/{created_task["id"]}', json=update_fields).json()
#     assert updated_task["title"] == update_fields["title"]


# def test_update_task_should_ignore_unknown_fields():
#     task = {"title": "Title", "description": "Description"}
#     created_task = client.post("/tasks", json=task).json()

#     update_fields = {"unknown_field": "Field"}
#     updated_task = client.put(f'/tasks/{created_task["id"]}', json=update_fields).json()
#     assert "unknown_field" not in updated_task.keys()


# def test_update_task_should_return_status_200_if_successful():
#     task = {"title": "Title", "description": "Description"}
#     created_task = client.post("/tasks", json=task).json()
#     print(created_task)

#     update_fields = {"unknown_field": "Field"}
#     response = client.put(f'/tasks/{created_task["id"]}', json=update_fields)
#     assert response.status_code == 200
