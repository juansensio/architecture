import pytest
from unittest.mock import patch
from src.application.todo.DeleteTodo import DeleteTodo
from fastapi.testclient import TestClient
from src.domain.todo.todo import Todo
from src.domain.todo.errors import TodoNotFoundError

from main import app

client = TestClient(app)


@pytest.fixture
def url():
    return '/todos'


@pytest.fixture
def todo():
    return Todo(
        uid='test',
        id='test1',
        content='test1'
    )


@patch.object(DeleteTodo, '__call__')
def test_delete_todo(mock_delete_todo, url, todo):
    message = 'success'
    mock_delete_todo.return_value = DeleteTodo.Outputs(message=message)
    response = client.delete(
        f"{url}/{todo.id}", headers={'Authorization': 'Bearer test'})
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == message


@patch.object(DeleteTodo, '__call__')
def test_should_fail_if_todo_does_not_exist(mock_delete_todo, url, todo):
    mock_delete_todo.side_effect = TodoNotFoundError()
    response = client.delete(
        f"{url}/{todo.id}", headers={'Authorization': 'Bearer test'})
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == TodoNotFoundError().message
