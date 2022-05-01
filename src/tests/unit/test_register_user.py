import pytest
from unittest import mock
import uuid

from src.domain.user.errors import UserAlreadyExistsError
from src.application.user.RegisterUser import RegisterUser


@pytest.fixture
def user():
    return {
        'uid': str(uuid.uuid4()),
        'username': 'test',
        'password': 'test'
    }


def test_register_user(user):
    repo = mock.Mock()
    repo.persist.return_value = user
    repo.find_one_by_name.return_value = False
    register_user = RegisterUser(repo)
    inputs = RegisterUser.Inputs(user=user)
    result = register_user(inputs)
    repo.persist.assert_called_once_with(user)
    repo.find_one_by_name.assert_called_once_with(user['username'])
    assert result.user == user


def test_raises_exception_if_user_already_exists(user):
    repo = mock.Mock()
    repo.find_one_by_name.return_value = True
    register_user = RegisterUser(repo)
    inputs = RegisterUser.Inputs(user=user)
    with pytest.raises(UserAlreadyExistsError):
        result = register_user(inputs)
