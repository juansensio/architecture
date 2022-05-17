import pytest
from unittest.mock import patch
from src.application.todo.RetrieveTodos import RetrieveTodos
from fastapi.testclient import TestClient
from src.domain.todo.todo import Todo
from src.domain.todo.errors import TodoNotFoundError

from main import app

client = TestClient(app)


@pytest.fixture
def url():
    return '/todos'


@pytest.fixture
def todos():
    return [
        Todo(
            uid='test',
            id='test1',
            content='test1'
        ),
        Todo(
            uid='test',
            id='test2',
            content='test2'
        ),
        Todo(
            uid='test',
            id='test3',
            content='test3'
        ),
    ]


@patch.object(RetrieveTodos, '__call__')
def test_retrieve_todos(mock_retrieve_todos, url, todos):
    mock_retrieve_todos.return_value = RetrieveTodos.Outputs(todos=todos)
    response = client.get(url, headers={'Authorization': 'Bearer test'})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for item, todo in zip(data, todos):
        assert item == todo.dict()


@patch.object(RetrieveTodos, '__call__')
def test_should_fail_if_todo_does_not_exist(mock_create_todo, url):
    mock_create_todo.side_effect = TodoNotFoundError()
    response = client.get(url, headers={'Authorization': 'Bearer test'})
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == TodoNotFoundError().message
