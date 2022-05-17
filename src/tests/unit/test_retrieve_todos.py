import pytest
from unittest import mock

from src.application.todo.RetrieveTodos import RetrieveTodos
from src.domain.todo.errors import TodoNotFoundError
from src.domain.user.user import User


@pytest.fixture
def todos():
    return [
        {
            'uid': 'test',
            'id': 'test',
            'content': 'test content'
        },
        {
            'uid': 'test2',
            'id': 'test2',
            'content': 'test content 2'
        },
    ]


def test_retrieve_todos(todos):
    repo = mock.Mock()
    user_repo = mock.Mock()
    user_repo.retrieve.return_value = User(
        **{'uid': '123', 'username': '123', 'password': '123', 'todos': [todo['id'] for todo in todos]})
    repo.retrieve.return_value = todos[0]
    repo.exists.return_value = True
    retrieve_todos = RetrieveTodos(repo, user_repo)
    inputs = RetrieveTodos.Inputs(uid='test')
    result = retrieve_todos(inputs)
    assert repo.retrieve.call_count == len(todos)
    assert repo.exists.call_count == len(todos)
    user_repo.retrieve.assert_called_once()
    assert len(result.todos) == len(todos)
    for todo in result.todos:
        assert todo == todos[0]


def test_should_fail_if_todo_does_not_exist(todos):
    repo = mock.Mock()
    user_repo = mock.Mock()
    user_repo.retrieve.return_value = User(
        **{'uid': '123', 'username': '123', 'password': '123', 'todos': [todo['id'] for todo in todos]})
    repo.exists.return_value = False
    retrieve_todos = RetrieveTodos(repo, user_repo)
    inputs = RetrieveTodos.Inputs(uid='test')
    with pytest.raises(TodoNotFoundError):
        retrieve_todos(inputs)


def test_should_return_empty_list_if_no_ids():
    repo = mock.Mock()
    user_repo = mock.Mock()
    user_repo.retrieve.return_value = User(
        **{'uid': '123', 'username': '123', 'password': '123', 'todos': []})
    retrieve_todos = RetrieveTodos(repo, user_repo)
    inputs = RetrieveTodos.Inputs(uid='test')
    result = retrieve_todos(inputs)
    assert repo.retrieve.call_count == 0
    assert len(result.todos) == 0
    assert result.todos == []
