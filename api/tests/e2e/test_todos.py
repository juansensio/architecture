import pytest
from src.domain.user.errors import UserNotFoundError
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def token():
    user = {
        'username': 'test_todos',
        'password': 'test'
    }
    # register user
    response = client.get(
        '/users/register', params={'username': user['username'], 'password': user['password']})
    # user login
    response = client.post(
        '/token', data={'username': user['username'], 'password': user['password']})
    return response.json()['access_token']


def test_crud_todos(token):
    content = 'test content'
    # create a todo item
    response = client.post(
        '/todos', json={'content': content}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json()['content'] == content
    # should fail if user exists
    response = client.post(
        '/todos', json={'content': content}, headers={'Authorization': f'Bearer invalid'})
    assert response.status_code == 400
    assert response.json()['detail'] == UserNotFoundError().message
    # retrieve todos
    # response = client.get(
    #     '/todos', headers={'Authorization': f'Bearer {token}'})
    # print(response.json())
    # assert response.status_code == 200
    # todos = response.json()
    # assert len(todos) == 1
    # assert todos[0]['content'] == content
