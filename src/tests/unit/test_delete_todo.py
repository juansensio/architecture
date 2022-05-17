import pytest
from unittest import mock

from src.application.todo.DeleteTodo import DeleteTodo
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


def test_delete_todo(todos):
    repo = mock.Mock()
    user_repo = mock.Mock()
    todo = todos[0]
    delete_todo = DeleteTodo(repo, user_repo)
    inputs = delete_todo.Inputs(uid=todo['uid'], id=todo['id'])
    result = delete_todo(inputs)
    repo.exists.assert_called_once_with(todo['id'])
    repo.delete.assert_called_once_with(todo['id'])
    user_repo.remove_todo.assert_called_once_with(todo['uid'], todo['id'])
    assert result.message == 'todo deleted'


def test_should_fail_if_todo_does_not_exist(todos):
    repo = mock.Mock()
    user_repo = mock.Mock()
    repo.exists.return_value = False
    delete_todo = DeleteTodo(repo, user_repo)
    inputs = delete_todo.Inputs(uid='123', id='invalid')
    with pytest.raises(TodoNotFoundError):
        delete_todo(inputs)
