import pytest
import uuid
from copy import deepcopy

from src.infrastructure.todo.TodoMemRepo import TodoMemRepo


@pytest.fixture
def todo_dicts():
    return [
        {
            'uid': str(uuid.uuid4()),
            'id': str(uuid.uuid4()),
            'content': 'test content'
        },
        {
            'uid': str(uuid.uuid4()),
            'id': str(uuid.uuid4()),
            'content': 'test content 2',
        }
    ]


@pytest.fixture
def todo():
    return {
        'uid': str(uuid.uuid4()),
        'id': str(uuid.uuid4()),
        'content': 'test content 3',
    }


def test_todo_persists(todo_dicts, todo):
    repo = TodoMemRepo(todo_dicts)
    repo.persist(todo)
    assert len(repo.data) == 3
    assert repo.data[0] == todo_dicts[0]
    assert repo.data[1] == todo_dicts[1]
    assert repo.data[2] == todo


def test_todo_retrieve(todo_dicts):
    repo = TodoMemRepo(todo_dicts)
    data = repo.retrieve(todo_dicts[0]['id'])
    assert data == todo_dicts[0]
    data = repo.retrieve(todo_dicts[1]['id'])
    assert data == todo_dicts[1]
    data = repo.retrieve('123')
    assert data == None


def test_todo_update(todo_dicts):
    repo = TodoMemRepo(todo_dicts)
    new_todo = deepcopy(todo_dicts[0])
    new_todo['content'] = 'new content'
    repo.update(new_todo)
    print(repo.data, todo_dicts)
    assert len(repo.data) == 2
    assert repo.data[1] == todo_dicts[1]
    assert repo.data[0]['uid'] == todo_dicts[0]['uid']
    assert repo.data[0]['id'] == todo_dicts[0]['id']
    assert repo.data[0]['content'] == 'new content'
