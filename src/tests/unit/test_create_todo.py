import pytest
from unittest import mock
import uuid

from src.application.todo.CreateTodo import CreateTodo
from src.domain.todo.todo import Todo
from src.domain.user.errors import UserNotFoundError


@pytest.fixture
def todo():
    return {
        'uid': 'test',
        'content': 'test content'
    }


def test_create_todo(todo):
    repo = mock.Mock()
    user_repo = mock.Mock()
    id = str(uuid.uuid4())
    repo.generate_id.return_value = id
    create_todo = CreateTodo(repo, user_repo)
    inputs = CreateTodo.Inputs(**todo)
    result = create_todo(inputs)
    repo.persist.assert_called_once_with({
        'uid': todo['uid'],
        'content': todo['content'],
        'id': id
    })
    repo.generate_id.assert_called_once()
    user_repo.exists.assert_called_once()
    user_repo.add_todo.assert_called_once_with(todo['uid'], id)
    assert result.content == todo['content']
    assert result.id == id


def test_should_fail_if_user_does_not_exist(todo):
    repo = mock.Mock()
    user_repo = mock.Mock()
    user_repo.exists.return_value = False
    create_todo = CreateTodo(repo, user_repo)
    inputs = CreateTodo.Inputs(**todo)
    with pytest.raises(UserNotFoundError):
        create_todo(inputs)
