import pytest
from unittest.mock import patch
from src.application.todo.UpdateTodo import UpdateTodo
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


@patch.object(UpdateTodo, '__call__')
def test_update_todo(mock_update_todo, url, todo):
    new_content = 'new content'
    mock_update_todo.return_value = UpdateTodo.Outputs(
        todo=Todo(id=todo.id, uid=todo.uid, content=new_content))
    response = client.put(
        f"{url}/{todo.id}", json={'content': new_content}, headers={'Authorization': 'Bearer test'})
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == todo.id
    assert data['content'] == new_content


@patch.object(UpdateTodo, '__call__')
def test_should_fail_if_todo_does_not_exist(mock_update_todo, url):
    mock_update_todo.side_effect = TodoNotFoundError()
    response = client.put(
        f"{url}/invalid", json={'content': 'new ciontent'}, headers={'Authorization': 'Bearer test'})
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == TodoNotFoundError().message
