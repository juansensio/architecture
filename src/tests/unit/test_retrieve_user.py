import pytest
from unittest import mock
import uuid

from src.domain.user.user import User
from src.domain.user.errors import UserNotFoundError, InvalidCredentialsError
from src.application.user.RetrieveUser import RetrieveUser


@pytest.fixture
def user():
    return {
        'uid': 'test',
        'username': 'test',
        'password': 'test',
        'todos': []
    }


def test_retrieve_user(user):
    repo = mock.Mock()
    repo.find_one_by_name.return_value = user
    retrieve_user = RetrieveUser(repo)
    inputs = RetrieveUser.Inputs(
        username=user['username'], password=user['password'])
    result = retrieve_user(inputs)
    repo.find_one_by_name.assert_called_once_with(user['username'])
    assert result.user.username == user['username']
    assert result.user.password == user['password']
    assert result.user.uid == user['uid']
    assert result.user.todos == user['todos']


def test_raises_exception_if_user_not_found(user):
    repo = mock.Mock()
    repo.find_one_by_name.return_value = None
    retrieve_user = RetrieveUser(repo)
    inputs = RetrieveUser.Inputs(
        username=user['username'], password=user['password'])
    with pytest.raises(UserNotFoundError) as e:
        retrieve_user(inputs)
    assert str(e.value) == 'User not found'


def test_raises_exception_if_invalid_password(user):
    repo = mock.Mock()
    repo.find_one_by_name.return_value = user
    retrieve_user = RetrieveUser(repo)
    inputs = RetrieveUser.Inputs(
        username=user['username'], password='invalid')
    with pytest.raises(InvalidCredentialsError) as e:
        retrieve_user(inputs)
    assert str(e.value) == 'Invalid credentials'
