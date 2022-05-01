import uuid
from src.domain.user.user import User
import pytest


def test_user_model():
    uid = str(uuid.uuid4())
    username = 'test_user'
    password = 'test_password'
    user = User(uid=uid, username=username, password=password)
    assert user.uid == uid
    assert user.username == username
    assert user.password == password


def test_user_model_from_dict():
    uid = str(uuid.uuid4())
    username = 'test_user'
    password = 'test_password'
    user_data = {
        'uid': uid,
        'username': username,
        'password': password
    }
    user = User(**user_data)
    assert user.uid == uid
    assert user.username == username
    assert user.password == password


def test_user_model_to_dict():
    uid = str(uuid.uuid4())
    username = 'test_user'
    password = 'test_password'
    user_data = {
        'uid': uid,
        'username': username,
        'password': password
    }
    user = User(**user_data)
    user_dict = user.dict()
    assert user_dict['uid'] == uid
    assert user_dict['username'] == username
    assert user_dict['password'] == password


def test_user_model_comparison():
    uid = str(uuid.uuid4())
    username = 'test_user'
    password = 'test_password'
    user_data = {
        'uid': uid,
        'username': username,
        'password': password
    }
    user1 = User(**user_data)
    user2 = User(**user_data)
    assert user1 == user2


def test_user_model_should_fail_on_missing_uid():
    username = 'test_user'
    password = 'test_password'
    user_data = {
        'username': username,
        'password': password
    }
    with pytest.raises(ValueError):
        user = User(**user_data)


def test_user_model_should_fail_on_missing_username():
    uid = str(uuid.uuid4())
    password = 'test_password'
    user_data = {
        'uid': uid,
        'password': password
    }
    with pytest.raises(ValueError):
        user = User(**user_data)


def test_user_model_should_fail_on_missing_password():
    uid = str(uuid.uuid4())
    username = 'test_user'
    user_data = {
        'uid': uid,
        'username': username,
    }
    with pytest.raises(ValueError):
        user = User(**user_data)


# def test_user_model_should_fail_on_invalid_username():
#     uid = str(uuid.uuid4())
#     username = True
#     password = 'test_password'
#     user_data = {
#         'uid': uid,
#         'username': username,
#         'password': password
#     }
#     with pytest.raises(ValueError):
#         user = User(**user_data)
