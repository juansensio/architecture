import pytest
import uuid

from src.infrastructure.MemRepo import MemRepo


@pytest.fixture
def user_dicts():
    return [
        {
            'uid': str(uuid.uuid4()),
            'username': 'test_user',
            'password': 'test_password'
        },
        {
            'uid': str(uuid.uuid4()),
            'username': 'test_user2',
            'password': 'test_password2'
        }
    ]


@pytest.fixture
def user():
    return {
        'uid': str(uuid.uuid4()),
        'username': 'test_user3',
        'password': 'test_password3'
    }


def test_data_persists(user_dicts, user):
    repo = MemRepo(user_dicts)
    result = repo.persist(user)
    assert result == user
    assert len(repo.data) == len(user_dicts)


def test_find_one_by_name(user_dicts):
    repo = MemRepo(user_dicts)
    user = user_dicts[0]
    result = repo.find_one_by_field('username', user['username'])
    assert result == user


def test_should_return_None_if_not_find_one_by_name(user_dicts, user):
    repo = MemRepo(user_dicts)
    result = repo.find_one_by_field('username', user['username'])
    assert result == None
