import uuid
from src.domain.user.user import User
from src.domain.todo.todo import Todo
import pytest


@pytest.fixture
def todos():
    return [
        str(uuid.uuid4()),
        str(uuid.uuid4()),
        str(uuid.uuid4())
    ]


def test_user_model(todos):
    uid = str(uuid.uuid4())
    username = 'test_user'
    password = 'test_password'
    user = User(uid=uid, username=username, password=password, todos=todos)
    assert user.uid == uid
    assert user.username == username
    assert user.password == password
    assert user.todos == todos


def test_user_model_from_dict(todos):
    uid = str(uuid.uuid4())
    username = 'test_user'
    password = 'test_password'
    user_data = {
        'uid': uid,
        'username': username,
        'password': password,
        'todos': todos
    }
    user = User(**user_data)
    assert user.uid == uid
    assert user.username == username
    assert user.password == password
    assert user.todos == todos


def test_user_model_to_dict(todos):
    uid = str(uuid.uuid4())
    username = 'test_user'
    password = 'test_password'
    user_data = {
        'uid': uid,
        'username': username,
        'password': password,
        'todos': todos
    }
    user = User(**user_data)
    user_dict = user.dict()
    assert user_dict['uid'] == uid
    assert user_dict['username'] == username
    assert user_dict['password'] == password
    assert user_dict['todos'] == todos


def test_user_model_comparison(todos):
    uid = str(uuid.uuid4())
    username = 'test_user'
    password = 'test_password'
    user_data = {
        'uid': uid,
        'username': username,
        'password': password,
        'todos': todos
    }
    user1 = User(**user_data)
    user2 = User(**user_data)
    assert user1 == user2


def test_user_model_should_fail_on_missing_uid(todos):
    username = 'test_user'
    password = 'test_password'
    user_data = {
        'username': username,
        'password': password,
        'todos': todos
    }
    with pytest.raises(ValueError):
        user = User(**user_data)


def test_user_model_should_fail_on_missing_username(todos):
    uid = str(uuid.uuid4())
    password = 'test_password'
    user_data = {
        'uid': uid,
        'password': password,
        'todos': todos
    }
    with pytest.raises(ValueError):
        user = User(**user_data)


def test_user_model_should_fail_on_missing_password(todos):
    uid = str(uuid.uuid4())
    username = 'test_user'
    user_data = {
        'uid': uid,
        'username': username,
        'todos': todos
    }
    with pytest.raises(ValueError):
        user = User(**user_data)


def test_user_model_should_fail_on_missing_todos():
    with pytest.raises(ValueError):
        User(**{
            'uid': str(uuid.uuid4()),
            'username': 'test_user',
            'password': 'test password',
        })


def test_user_model_should_fail_on_invalid_todos():
    with pytest.raises(ValueError):
        User(**{
            'uid': str(uuid.uuid4()),
            'username': 'test_user',
            'password': 'test password',
            'todos': 'test'
        })
