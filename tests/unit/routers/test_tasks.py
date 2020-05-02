from starlette.status import HTTP_200_OK
from unittest.mock import patch
from uuid import UUID

from app.enums import TaskStatus
from app.models import Task
from app.repositories import TasksRepository
from app.schemas import Task as TaskSchema


default_task = Task(
    id=UUID("e006c329-2dc8-41c3-bd4d-3611e300e0e8"),
    title="title",
    description="description",
    status=TaskStatus.TODO,
)

done_task = Task(
    id=UUID("0360de95-6001-4236-a56a-58e1bbecdbb9"),
    title="title",
    description="description",
    status=TaskStatus.DONE,
)

new_task = {
    "title": "title",
    "description": "description",
}


@patch.object(TasksRepository, "get_all", return_value=[default_task])
def test_task_list_should_return_status_200(mock_get_all, client):
    response = client.get("/tasks")
    assert response.status_code == HTTP_200_OK


@patch.object(TasksRepository, "get_all", return_value=[default_task])
def test_task_list_should_return_json(mock_get_all, client):
    response = client.get("/tasks")
    assert response.headers["Content-Type"] == "application/json"


@patch.object(TasksRepository, "get_all", return_value=[default_task])
def test_task_list_should_return_list(mock_get_all, client):
    response = client.get("/tasks")
    assert isinstance(response.json(), list)


@patch.object(TasksRepository, "get_all", return_value=[default_task])
def test_listed_task_should_have_id(mock_get_all, client):
    response = client.get("/tasks")
    assert "id" in response.json().pop()


@patch.object(TasksRepository, "get_all", return_value=[default_task])
def test_listed_task_should_have_title(mock_get_all, client):
    response = client.get("/tasks")
    assert "title" in response.json().pop()


@patch.object(TasksRepository, "get_all", return_value=[default_task])
def test_listed_task_should_have_description(mock_get_all, client):
    response = client.get("/tasks")
    assert "description" in response.json().pop()


@patch.object(TasksRepository, "get_all", return_value=[default_task])
def test_listed_task_should_have_status(mock_get_all, client):
    response = client.get("/tasks")
    assert "status" in response.json().pop()


@patch.object(TasksRepository, "get_all", return_value=[done_task, default_task])
def test_listed_tasks_should_be_ordered_by_status_todo(mock_get_all, client):
    response = client.get("/tasks")
    assert response.json()[0]["status"] == "TODO"


def test_task_endpoint_should_accept_post(client):
    response = client.post("/tasks")
    assert response.status_code != 405


def test_task_should_have_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 422


def test_task_title_should_have_at_least_3_characters(client):
    response = client.post("/tasks", json={"title": 2 * "*"})
    assert response.status_code == 422


def test_task_title_should_have_at_most_50_characters(client):
    response = client.post("/tasks", json={"title": 51 * "*"})
    assert response.status_code == 422


def test_task_should_have_description(client):
    response = client.post("/tasks", json={"title": "Title"})
    assert response.status_code == 422


def test_task_description_should_have_at_most_140_characters(client):
    response = client.post("/tasks", json={"title": "Title", "description": "*" * 141})
    assert response.status_code == 422


@patch.object(TasksRepository, "create", return_value=default_task)
def test_created_task_should_be_returned(mock_create, client):
    response = client.post("/tasks", json=new_task)
    assert response.json()["title"] == new_task["title"]
    assert response.json()["description"] == new_task["description"]


@patch.object(TasksRepository, "create", return_value=default_task)
def test_created_task_should_have_default_status_todo(mock_create, client):
    response = client.post("/tasks", json=new_task)
    assert response.json()["status"] == "TODO"


@patch.object(TasksRepository, "create", return_value=default_task)
def test_created_task_should_return_status_201(mock_create, client):
    response = client.post("/tasks", json=new_task)
    assert response.status_code == 201


def test_delete_task_endpoint_should_accept_delete(client):
    response = client.delete("/tasks/task_id")
    assert response.status_code != 405


@patch.object(TasksRepository, "delete")
def test_delete_task_should_return_status_204(mock_delete, client):
    response = client.delete(f"/tasks/{default_task.id}")
    assert response.status_code == 204


def test_delete_task_should_return_status_404_if_task_not_found(client):
    response = client.delete("/tasks/8415b9a1-cca3-40c2-af7b-1ad689889fba")
    assert response.status_code == 404


def test_read_task_endpoint_should_accept_get(client):
    response = client.get("/tasks/task_id")
    assert response.status_code != 405


def test_read_task_should_return_status_404_if_task_not_found(client):
    response = client.get("/tasks/8415b9a1-cca3-40c2-af7b-1ad689889fba")
    assert response.status_code == 404


@patch.object(TasksRepository, "get_by_id", return_value=default_task)
def test_read_task_should_return_status_200_if_task_found(mock_get_by_id, client):
    response = client.get(f"/tasks/{default_task.id}")
    assert response.status_code == 200


@patch.object(TasksRepository, "get_by_id", return_value=default_task)
def test_read_task_should_return_task_if_found(mock_get_by_id, client):
    response = client.get(f"/tasks/{default_task.id}")
    assert response.json()["id"] == str(default_task.id)


def test_update_task_endpoint_should_accept_put(client):
    response = client.put("/tasks/task_id")
    assert response.status_code != 405


def test_update_task_should_return_status_404_if_task_not_found(client):
    task = {"title": "Title", "description": "Description"}
    response = client.put("/tasks/8415b9a1-cca3-40c2-af7b-1ad689889fba", json=task)
    assert response.status_code == 404


@patch.object(TasksRepository, "update", return_value=default_task)
def test_update_task_should_not_have_required_fields(mock_update, client):
    response = client.put(f"/tasks/{default_task.id}", json={})
    assert response.status_code != 422


@patch.object(TasksRepository, "update", return_value=default_task)
def test_update_task_should_return_updated_task(mock_update, client):
    updated_task = client.put(f"/tasks/{default_task.id}", json={}).json()
    assert TaskSchema.parse_obj(updated_task) == TaskSchema.from_orm(default_task)


@patch.object(TasksRepository, "update", return_value=default_task)
def test_update_task_should_ignore_unknown_fields(mock_update, client):
    update_fields = {"title": "New title", "unknown_field": "Field"}
    client.put(f"/tasks/{default_task.id}", json=update_fields)
    mock_update.assert_called_once_with(default_task.id, {"title": "New title"})


@patch.object(TasksRepository, "update", return_value=default_task)
def test_update_task_should_return_status_200_if_successful(mock_update, client):
    response = client.put(f"/tasks/{default_task.id}", json={})
    assert response.status_code == 200
