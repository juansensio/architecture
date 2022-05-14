import pytest
from unittest.mock import patch
from src.application.todo.CreateTodo import CreateTodo
from fastapi.testclient import TestClient
from src.domain.todo.todo import Todo
from src.domain.user.errors import UserNotFoundError

from main import app

client = TestClient(app)


@pytest.fixture
def url():
    return '/todos'


@pytest.fixture
def todo():
    return Todo(
        uid='test',
        id='test',
        content='test'
    )


@patch.object(CreateTodo, '__call__')
def test_create_todo(mock_create_todo, url, todo):
    mock_create_todo.return_value = CreateTodo.Outputs(
        id=todo.id, content=todo.content)
    response = client.post(
        url, json={'content': todo.content}, headers={'Authorization': 'Bearer test'})
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == todo.id
    assert data['content'] == todo.content


@patch.object(CreateTodo, '__call__')
def test_should_fail_if_user_does_not_exist(mock_create_todo, url, todo):
    mock_create_todo.side_effect = UserNotFoundError()
    response = client.post(
        url, json={'content': todo.content}, headers={'Authorization': 'Bearer test'})
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == UserNotFoundError().message
