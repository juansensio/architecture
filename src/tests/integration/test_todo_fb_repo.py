from src.infrastructure.todo.TodoFirebaseRepo import TodoFirebaseRepo
from src.domain.todo.todo import Todo
import pytest
import uuid
from copy import deepcopy

from src.infrastructure.shared.FirebaseRepo import init_db

name = 'todos-test'
collection = 'todos-test'

todos_dicts = [
    {
        'uid': str(uuid.uuid4()),
        'id': str(uuid.uuid4()),
        'content': 'test content',

    },
    {
        'uid': str(uuid.uuid4()),
        'id': str(uuid.uuid4()),
        'content': 'test content 2',
    }
]


@pytest.fixture(scope='module')
def db():
    # import warnings
    # warnings.filterwarnings("ignore", category=DeprecationWarning)
    db = init_db(name, creds='./infrastructure/shared/firebase.json')
    for d in todos_dicts:
        doc = db.collection(collection).document()
        d['id'] = doc.id
        doc.set(d)
    yield db
    docs = db.collection(collection).stream()
    for doc in docs:
        doc.reference.delete()


@pytest.fixture
def todo():
    return {
        'uid': str(uuid.uuid4()),
        'id': str(uuid.uuid4()),
        'content': 'test content 3',
    }


# @pytest.mark.filterwarnings("ignore:Call to deprecated")
def test_todo_generate_id(db):
    repo = TodoFirebaseRepo(name, collection)
    assert repo.generate_id() != None


def test_todo_retrieve(db):
    repo = TodoFirebaseRepo(name, collection)
    data = repo.retrieve(todos_dicts[0]['id'])
    assert data == todos_dicts[0]
    data = repo.retrieve(todos_dicts[1]['id'])
    assert data == todos_dicts[1]
    data = repo.retrieve('123')
    assert data == None


def test_todo_update(db):
    repo = TodoFirebaseRepo(name, collection)
    new_todo = deepcopy(todos_dicts[0])
    new_todo['content'] = 'new content'
    repo.update(new_todo)
    data = repo.retrieve(new_todo['id'])
    assert data == new_todo


def test_todo_delete(db):
    assert len(list(db.collection(collection).stream())) == len(todos_dicts)
    repo = TodoFirebaseRepo(name, collection)
    repo.delete(todos_dicts[0]['id'])
    data = repo.retrieve(todos_dicts[0]['id'])
    assert data == None
    assert len(list(db.collection(collection).stream())
               ) == len(todos_dicts) - 1
