import pytest
from unittest import mock

from src.application.todo.UpdateTodo import UpdateTodo
from src.domain.todo.errors import TodoNotFoundError


@pytest.fixture
def todos():
    return [
        {
            'uid': 'test1',
            'id': 'test1',
            'content': 'test content 1'
        },
        {
            'uid': 'test2',
            'id': 'test2',
            'content': 'test content 2'
        },
    ]


@pytest.fixture
def new_todo():
    return {
        'id': 'test1',
        'new_content': 'test content 3'
    }


def test_update_todo(todos, new_todo):
    repo = mock.Mock()
    update_todo = UpdateTodo(repo)
    todo = todos[0]
    repo.retrieve.return_value = todo
    inputs = update_todo.Inputs(**new_todo)
    result = update_todo(inputs)
    repo.exists.assert_called_once_with(todo['id'])
    todo.update(content=new_todo['new_content'])
    assert result.todo.dict() == todo


def test_should_fail_if_todo_does_not_exist(todos, new_todo):
    repo = mock.Mock()
    repo.exists.return_value = False
    update_todo = UpdateTodo(repo)
    inputs = update_todo.Inputs(**new_todo)
    with pytest.raises(TodoNotFoundError):
        update_todo(inputs)
