import pytest
import uuid

from src.infrastructure.user.UserMemRepo import UserMemRepo


@pytest.fixture
def user_dicts():
    return [
        {
            'uid': str(uuid.uuid4()),
            'username': 'test_user',
            'password': 'test_password',
            'todos': [],
        },
        {
            'uid': str(uuid.uuid4()),
            'username': 'test_user2',
            'password': 'test_password2',
            'todos': [],
        }
    ]


@pytest.fixture
def user():
    return {
        'uid': str(uuid.uuid4()),
        'username': 'test_user3',
        'password': 'test_password3',
        'todos': [],
    }


@pytest.fixture
def todo():
    return {
        'uid': str(uuid.uuid4()),
        'id': str(uuid.uuid4()),
        'content': 'test content',
    }


def test_user_find_one_by_name(user_dicts, user):
    repo = UserMemRepo(user_dicts)
    assert repo.find_one_by_name(user_dicts[0]['username']) == user_dicts[0]
    assert repo.find_one_by_name(user_dicts[1]['username']) == user_dicts[1]
    assert repo.find_one_by_name(user['username']) == None


def test_user_persists(user_dicts, user):
    repo = UserMemRepo(user_dicts)
    repo.persist(user)
    assert len(repo.data) == 3
    assert repo.data[0] == user_dicts[0]
    assert repo.data[1] == user_dicts[1]
    assert repo.data[2] == user


def test_add_todo(user_dicts, todo):
    repo = UserMemRepo(user_dicts)
    repo.add_todo(user_dicts[0]['uid'], todo['id'])
    assert len(repo.data) == 2
    assert repo.data[0] == user_dicts[0]
    assert repo.data[1] == user_dicts[1]
    assert len(repo.data[0]['todos']) == 1
    assert repo.data[0]['todos'][0] == todo['id']


def test_user_exists(user_dicts, user):
    repo = UserMemRepo(user_dicts)
    assert repo.exists(user_dicts[0]['uid']) == True
    assert repo.exists(user_dicts[1]['uid']) == True
    assert repo.exists(user['uid']) == False
