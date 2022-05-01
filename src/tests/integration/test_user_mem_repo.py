import pytest
import uuid

from src.infrastructure.user.UserMemRepo import UserMemRepo
from src.application.user.RegisterUser import RegisterUser
from src.domain.user.errors import UserAlreadyExistsError


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


def test_user_persists(user_dicts, user):
    repo = UserMemRepo(user_dicts)
    register_user = RegisterUser(repo)
    inputs = RegisterUser.Inputs(user=user)
    result = register_user(inputs)
    assert result.user == user
    assert len(repo.data) == 3


def test_should_fail_if_user_exists(user_dicts):
    repo = UserMemRepo(user_dicts)
    user = user_dicts[0]
    register_user = RegisterUser(repo)
    inputs = RegisterUser.Inputs(user=user)
    with pytest.raises(UserAlreadyExistsError):
        result = register_user(inputs)
