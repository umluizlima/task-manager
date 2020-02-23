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
    task = {
        "id": "8415b9a1-cca3-40c2-af7b-1ad689889fba",
        "title": "Title",
        "description": "Description",
    }
    TASKS.append(task)
    client = TestClient(app)
    response = client.get("/tasks")
    assert "id" in response.json().pop()
    TASKS.clear()


def test_listed_task_should_have_title():
    task = {
        "id": "8415b9a1-cca3-40c2-af7b-1ad689889fba",
        "title": "Title",
        "description": "Description",
    }
    TASKS.append(task)
    client = TestClient(app)
    response = client.get("/tasks")
    assert "title" in response.json().pop()
    TASKS.clear()


def test_listed_task_should_have_description():
    task = {
        "id": "8415b9a1-cca3-40c2-af7b-1ad689889fba",
        "title": "Title",
        "description": "Description",
    }
    TASKS.append(task)
    client = TestClient(app)
    response = client.get("/tasks")
    assert "description" in response.json().pop()
    TASKS.clear()


def test_listed_task_should_have_status():
    task = {
        "id": "8415b9a1-cca3-40c2-af7b-1ad689889fba",
        "title": "Title",
        "description": "Description",
    }
    TASKS.append(task)
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
    response = client.post("/tasks", json={"title": "Title", "description": "*" * 141})
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


def test_created_task_should_have_default_status_todo():
    client = TestClient(app)
    task = {"title": "Title", "description": "Description"}
    response = client.post("/tasks", json=task)
    assert response.json()["status"] == "TODO"
    TASKS.clear()


def test_created_task_should_return_status_201():
    client = TestClient(app)
    task = {"title": "Title", "description": "Description"}
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


def test_delete_task_endpoint_should_accept_delete():
    client = TestClient(app)
    response = client.delete("/tasks/task_id")
    assert response.status_code != 405


def test_delete_task_should_return_status_204():
    client = TestClient(app)
    task = {"title": "Title", "description": "Description"}
    created_task = client.post("/tasks", json=task).json()
    response = client.delete(f'/tasks/{created_task["id"]}')
    assert response.status_code == 204
    TASKS.clear()


def test_delete_task_should_return_status_404_if_task_not_found():
    client = TestClient(app)
    response = client.delete("/tasks/8415b9a1-cca3-40c2-af7b-1ad689889fba")
    assert response.status_code == 404


def test_delete_task_should_remove_task_from_persistence():
    client = TestClient(app)
    task = {"title": "Title", "description": "Description"}
    created_task = client.post("/tasks", json=task).json()
    client.delete(f'/tasks/{created_task["id"]}')
    assert len(TASKS) == 0
    TASKS.clear()


def test_read_task_endpoint_should_accept_get():
    client = TestClient(app)
    response = client.get("/tasks/task_id")
    assert response.status_code != 405


def test_read_task_should_return_status_404_if_task_not_found():
    client = TestClient(app)
    response = client.get("/tasks/8415b9a1-cca3-40c2-af7b-1ad689889fba")
    assert response.status_code == 404


def test_read_task_should_return_status_200_if_task_found():
    client = TestClient(app)
    task = {"title": "Title", "description": "Description"}
    created_task = client.post("/tasks", json=task).json()
    response = client.get(f'/tasks/{created_task["id"]}')
    assert response.status_code == 200


def test_read_task_should_return_task_if_found():
    client = TestClient(app)
    task = {"title": "Title", "description": "Description"}
    created_task = client.post("/tasks", json=task).json()
    response = client.get(f'/tasks/{created_task["id"]}')
    assert response.json()["title"] == task["title"]
    assert response.json()["description"] == task["description"]
