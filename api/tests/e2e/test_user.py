import pytest
from src.domain.user.errors import UserAlreadyExistsError, UserNotFoundError, InvalidCredentialsError
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def user():
    return {
        'username': 'test_create',
        'password': 'test'
    }


def test_register_user(user):
    # register user
    response = client.get(
        '/users/register', params={'username': user['username'], 'password': user['password']})
    assert response.status_code == 200
    data = response.json()
    uid = data['uid']
    assert data['username'] == user['username']
    # user login
    response = client.post(
        '/token', data={'username': user['username'], 'password': user['password']})
    assert response.status_code == 200
    assert response.json()['access_token'] == uid
    # should fail if user exists
    response = client.get(
        '/users/register', params={'username': user['username'], 'password': user['password']})
    assert response.status_code == 400
    assert response.json()['detail'] == UserAlreadyExistsError().message
    # should fail if invalid username
    response = client.post(
        '/token', data={'username': 'invalid', 'password': user['password']})
    assert response.status_code == 400
    # should fail if invalid password
    assert response.json()['detail'] == UserNotFoundError().message
    response = client.post(
        '/token', data={'username': user['username'], 'password': 'invalid'})
    assert response.status_code == 400
    assert response.json()['detail'] == InvalidCredentialsError().message
