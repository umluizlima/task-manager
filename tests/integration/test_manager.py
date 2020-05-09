from os import environ
from subprocess import run

from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK
from testcontainers.postgres import PostgresContainer

from app import app
from app.enums import TaskStatus


client = TestClient(app)


@fixture(scope="module", autouse=True)
def setup():
    postgres_container = PostgresContainer("postgres:12.2")
    with postgres_container as postgres:
        environ["DATABASE_URL"] = postgres.get_connection_url()
        run(["alembic", "upgrade", "head"])
        yield


def test_task_list_should_return_status_200():
    response = client.get("/tasks")
    assert response.status_code == HTTP_200_OK


def test_task_list_should_return_json():
    response = client.get("/tasks")
    assert response.headers["Content-Type"] == "application/json"


def test_task_list_should_return_list():
    response = client.get("/tasks")
    assert isinstance(response.json(), list)


# def test_listed_task_should_have_id(tasks):
#     task = {
#         "id": "8415b9a1-cca3-40c2-af7b-1ad689889fba",
#         "title": "Title",
#         "description": "Description",
#         "status": TaskStatus.TODO,
#     }
#     tasks.append(task)
#     response = client.get("/tasks")
#     assert "id" in response.json().pop()


# def test_listed_task_should_have_title(tasks):
#     task = {
#         "id": "8415b9a1-cca3-40c2-af7b-1ad689889fba",
#         "title": "Title",
#         "description": "Description",
#         "status": TaskStatus.TODO,
#     }
#     tasks.append(task)
#     response = client.get("/tasks")
#     assert "title" in response.json().pop()


# def test_listed_task_should_have_description(tasks):
#     task = {
#         "id": "8415b9a1-cca3-40c2-af7b-1ad689889fba",
#         "title": "Title",
#         "description": "Description",
#         "status": TaskStatus.TODO,
#     }
#     tasks.append(task)
#     response = client.get("/tasks")
#     assert "description" in response.json().pop()


# def test_listed_task_should_have_status(tasks):
#     task = {
#         "id": "8415b9a1-cca3-40c2-af7b-1ad689889fba",
#         "title": "Title",
#         "description": "Description",
#         "status": TaskStatus.TODO,
#     }
#     tasks.append(task)
#     response = client.get("/tasks")
#     assert "status" in response.json().pop()


def test_listed_tasks_should_be_ordered_by_status_todo():
    task1 = {"title": "Title 1", "description": "Description1", "status": "DONE"}
    client.post("/tasks", json=task1)
    task2 = {"title": "Title 2", "description": "Description2", "status": "TODO"}
    client.post("/tasks", json=task2)
    response = client.get("/tasks")
    assert response.json()[0]["status"] == "TODO"


def test_task_endpoint_should_accept_post():
    response = client.post("/tasks")
    assert response.status_code != 405


def test_task_should_have_title():
    response = client.post("/tasks", json={})
    assert response.status_code == 422


def test_task_title_should_have_at_least_3_characters():
    response = client.post("/tasks", json={"title": 2 * "*"})
    assert response.status_code == 422


def test_task_title_should_have_at_most_50_characters():
    response = client.post("/tasks", json={"title": 51 * "*"})
    assert response.status_code == 422


def test_task_should_have_description():
    response = client.post("/tasks", json={"title": "Title"})
    assert response.status_code == 422


def test_task_description_should_have_at_most_140_characters():
    response = client.post("/tasks", json={"title": "Title", "description": "*" * 141})
    assert response.status_code == 422


def test_created_task_should_be_returned():
    task = {"title": "Title", "description": "Description"}
    response = client.post("/tasks", json=task)
    assert response.json()["title"] == task["title"]
    assert response.json()["description"] == task["description"]


def test_created_task_should_have_unique_id():
    task1 = {"title": "Title 1", "description": "Description1"}
    task2 = {"title": "Title 2", "description": "Description2"}
    response1 = client.post("/tasks", json=task1)
    response2 = client.post("/tasks", json=task2)
    assert response1.json()["id"] != response2.json()["id"]


def test_created_task_should_have_default_status_todo():
    task = {"title": "Title", "description": "Description"}
    response = client.post("/tasks", json=task)
    assert response.json()["status"] == "TODO"


def test_created_task_should_return_status_201():
    task = {"title": "Title", "description": "Description"}
    response = client.post("/tasks", json=task)
    assert response.status_code == 201


# def test_created_task_should_be_persisted(tasks):
#     task = {"title": "Title", "description": "Description"}
#     response = client.post("/tasks", json=task)
#     assert response.status_code == 201
#     assert len(tasks) == 1


def test_delete_task_endpoint_should_accept_delete():
    response = client.delete("/tasks/task_id")
    assert response.status_code != 405


def test_delete_task_should_return_status_204():
    task = {"title": "Title", "description": "Description"}
    created_task = client.post("/tasks", json=task).json()
    response = client.delete(f'/tasks/{created_task["id"]}')
    assert response.status_code == 204


def test_delete_task_should_return_status_404_if_task_not_found():
    response = client.delete("/tasks/8415b9a1-cca3-40c2-af7b-1ad689889fba")
    assert response.status_code == 404


# def test_delete_task_should_remove_task_from_persistence(tasks):
#     task = {"title": "Title", "description": "Description"}
#     created_task = client.post("/tasks", json=task).json()
#     client.delete(f'/tasks/{created_task["id"]}')
#     assert len(tasks) == 0


def test_read_task_endpoint_should_accept_get():
    response = client.get("/tasks/task_id")
    assert response.status_code != 405


def test_read_task_should_return_status_404_if_task_not_found():
    response = client.get("/tasks/8415b9a1-cca3-40c2-af7b-1ad689889fba")
    assert response.status_code == 404


def test_read_task_should_return_status_200_if_task_found():
    task = {"title": "Title", "description": "Description"}
    created_task = client.post("/tasks", json=task).json()
    response = client.get(f'/tasks/{created_task["id"]}')
    assert response.status_code == 200


def test_read_task_should_return_task_if_found():
    task = {"title": "Title", "description": "Description"}
    created_task = client.post("/tasks", json=task).json()
    response = client.get(f'/tasks/{created_task["id"]}')
    assert response.json()["title"] == task["title"]
    assert response.json()["description"] == task["description"]


def test_update_task_endpoint_should_accept_put():
    response = client.put("/tasks/task_id")
    assert response.status_code != 405


def test_update_task_should_return_status_404_if_task_not_found():
    task = {"title": "Title", "description": "Description"}
    response = client.put("/tasks/8415b9a1-cca3-40c2-af7b-1ad689889fba", json=task)
    assert response.status_code == 404


def test_update_task_should_not_have_required_fields():
    task = {"title": "Title", "description": "Description"}
    created_task = client.post("/tasks", json=task).json()

    update_fields = {}
    response = client.put(f'/tasks/{created_task["id"]}', json=update_fields)
    assert response.status_code != 422


def test_update_task_should_return_updated_task():
    task = {"title": "Title", "description": "Description"}
    created_task = client.post("/tasks", json=task).json()

    update_fields = {"title": "New title"}
    updated_task = client.put(f'/tasks/{created_task["id"]}', json=update_fields).json()
    assert updated_task["title"] == update_fields["title"]


def test_update_task_should_ignore_unknown_fields():
    task = {"title": "Title", "description": "Description"}
    created_task = client.post("/tasks", json=task).json()

    update_fields = {"unknown_field": "Field"}
    updated_task = client.put(f'/tasks/{created_task["id"]}', json=update_fields).json()
    assert "unknown_field" not in updated_task.keys()


def test_update_task_should_return_status_200_if_successful():
    task = {"title": "Title", "description": "Description"}
    created_task = client.post("/tasks", json=task).json()
    print(created_task)

    update_fields = {"unknown_field": "Field"}
    response = client.put(f'/tasks/{created_task["id"]}', json=update_fields)
    assert response.status_code == 200
