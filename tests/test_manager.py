from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK

from app import app, TASKS


def test_task_list_should_return_status_200():
    client = TestClient(app)
    response = client.get("/tasks")
    assert response.status_code == HTTP_200_OK


def test_task_list_should_return_json():
    client = TestClient(app)
    response = client.get("/tasks")
    assert response.headers["Content-Type"] == "application/json"


def test_task_list_should_return_list():
    client = TestClient(app)
    response = client.get("/tasks")
    assert isinstance(response.json(), list)


def test_listed_task_should_have_id():
    TASKS.append({"id": 1})
    client = TestClient(app)
    response = client.get("/tasks")
    assert "id" in response.json().pop()
    TASKS.clear()


def test_listed_task_should_have_title():
    TASKS.append({"title": "Title"})
    client = TestClient(app)
    response = client.get("/tasks")
    assert "title" in response.json().pop()
    TASKS.clear()


def test_listed_task_should_have_description():
    TASKS.append({"description": "Description"})
    client = TestClient(app)
    response = client.get("/tasks")
    assert "description" in response.json().pop()
    TASKS.clear()


def test_listed_task_should_have_status():
    TASKS.append({"status": "Done"})
    client = TestClient(app)
    response = client.get("/tasks")
    assert "status" in response.json().pop()
    TASKS.clear()
