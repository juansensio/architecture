import pytest
from unittest.mock import patch
from src.domain.user.user import User
from src.domain.user.errors import UserAlreadyExistsError
from src.application.user.RegisterUser import RegisterUser
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def url():
    return '/users/register'


@pytest.fixture
def user():
    return User(
        uid='test',
        username='test',
        password='test',
        todos=[]
    )


@patch.object(RegisterUser, '__call__')
def test_register_user(mock_register_user, url, user):
    mock_register_user.return_value = RegisterUser.Outputs(
        uid=user.uid, username=user.username, todos=user.todos)
    response = client.get(
        url, params={'username': user.username, 'password': user.password})
    assert response.status_code == 200
    data = response.json()
    assert data['uid'] == user.uid
    assert data['username'] == user.username
    assert data['todos'] == user.todos


@patch.object(RegisterUser, '__call__')
def test_register_user_should_fail_if_user_exists(mock_register_user, url, user):
    mock_register_user.side_effect = UserAlreadyExistsError()
    response = client.get(
        url, params={'username': user.username, 'password': user.password})
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == UserAlreadyExistsError().message
