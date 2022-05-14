import pytest
from unittest import mock

from src.application.todo.RetrieveTodos import RetrieveTodos
from src.domain.todo.errors import TodoNotFoundError


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
    repo.retrieve.return_value = todos[0]
    repo.exists.return_value = True
    todos_ids = [todo['id'] for todo in todos]
    retrieve_todos = RetrieveTodos(repo)
    inputs = RetrieveTodos.Inputs(ids=todos_ids)
    result = retrieve_todos(inputs)
    assert repo.retrieve.call_count == len(todos)
    assert len(result.todos) == len(todos)
    for todo in result.todos:
        assert todo == todos[0]


def test_should_fail_if_todo_does_not_exist(todos):
    repo = mock.Mock()
    repo.exists.return_value = False
    retrieve_todos = RetrieveTodos(repo)
    todos_ids = [todo['id'] for todo in todos]
    inputs = RetrieveTodos.Inputs(ids=todos_ids)
    with pytest.raises(TodoNotFoundError):
        retrieve_todos(inputs)


def test_should_return_empty_list_if_no_ids():
    repo = mock.Mock()
    retrieve_todos = RetrieveTodos(repo)
    inputs = RetrieveTodos.Inputs(ids=[])
    result = retrieve_todos(inputs)
    assert repo.retrieve.call_count == 0
    assert len(result.todos) == 0
    assert result.todos == []
