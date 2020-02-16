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


def test_task_endpoint_should_accept_post():
    client = TestClient(app)
    response = client.post("/tasks")
    assert response.status_code != 405


def test_task_should_have_title():
    client = TestClient(app)
    response = client.post("/tasks", json={})
    assert response.status_code == 422


def test_task_title_should_have_at_least_3_characters():
    client = TestClient(app)
    response = client.post("/tasks", json={"title": 2 * "*"})
    assert response.status_code == 422


def test_task_title_should_have_at_most_50_characters():
    client = TestClient(app)
    response = client.post("/tasks", json={"title": 51 * "*"})
    assert response.status_code == 422


def test_task_should_have_description():
    client = TestClient(app)
    response = client.post("/tasks", json={"title": "Title"})
    assert response.status_code == 422


def test_task_description_should_have_at_most_140_characters():
    client = TestClient(app)
    response = client.post(
        "/tasks",
        json={"title": "Title", "description": "*" * 141})
    assert response.status_code == 422


def test_created_task_should_be_returned():
    client = TestClient(app)
    task = {"title": "Title", "description": "Description"}
    response = client.post("/tasks", json=task)
    assert response.json()["title"] == task["title"]
    assert response.json()["description"] == task["description"]
    TASKS.clear()


def test_created_task_should_have_unique_id():
    client = TestClient(app)
    task1 = {"title": "Title 1", "description": "Description1"}
    task2 = {"title": "Title 2", "description": "Description2"}
    response1 = client.post("/tasks", json=task1)
    response2 = client.post("/tasks", json=task2)
    assert response1.json()["id"] != response2.json()["id"]
    TASKS.clear()


def test_created_task_should_have_default_status_open():
    client = TestClient(app)
    task = {"title": "Title", "description": "Description"}
    response = client.post("/tasks", json=task)
    assert response.json()["status"] == "OPEN"
    TASKS.clear()


def test_created_task_should_return_status_201():
    client = TestClient(app)
    task = {"title": "Titulo", "description": "Description"}
    response = client.post("/tasks", json=task)
    assert response.status_code == 201
    TASKS.clear()


def test_created_task_should_be_persisted():
    client = TestClient(app)
    task = {"title": "Title", "description": "Description"}
    response = client.post("/tasks", json=task)
    assert response.status_code == 201
    assert len(TASKS) == 1
    TASKS.clear()
