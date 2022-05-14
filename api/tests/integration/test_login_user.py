import pytest
from unittest.mock import patch
from src.domain.user.user import User
from src.domain.user.errors import UserNotFoundError, InvalidCredentialsError
from src.application.user.RetrieveUser import RetrieveUser
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def url():
    return '/token'


@pytest.fixture
def user():
    return User(
        uid='test',
        username='test',
        password='test',
        todos=[]
    )


@patch.object(RetrieveUser, '__call__')
def test_login_user(mock_retrieve_user, url, user):
    mock_retrieve_user.return_value = RetrieveUser.Outputs(user=user)
    response = client.post(
        url, data={'username': user.username, 'password': user.password})
    assert response.status_code == 200
    data = response.json()
    assert data['access_token'] == user.username
    assert data['token_type'] == 'bearer'


@patch.object(RetrieveUser, '__call__')
def test_login_user_should_fail_if_user_exists(mock_retrieve_user, url, user):
    mock_retrieve_user.side_effect = UserNotFoundError()
    response = client.post(
        url, data={'username': user.username, 'password': user.password})
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == UserNotFoundError().message


@patch.object(RetrieveUser, '__call__')
def test_login_user_should_fail_if_invalid_password(mock_retrieve_user, url, user):
    mock_retrieve_user.side_effect = InvalidCredentialsError()
    response = client.post(
        url, data={'username': user.username, 'password': user.password})
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == InvalidCredentialsError().message
