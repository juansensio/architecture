from dataclasses import dataclass
import uuid
from src.domain.todo.todo import Todo
import pytest


def test_todo_model():
    uid = str(uuid.uuid4())
    content = 'test'
    id = str(uuid.uuid4())
    todo = Todo(id=id, uid=uid, content=content)
    assert todo.uid == uid
    assert todo.content == content
    assert todo.id == id


def test_todo_model_from_dict():
    uid = str(uuid.uuid4())
    id = str(uuid.uuid4())
    content = 'tet'
    data = {
        'id': id,
        'uid': uid,
        'content': content,
    }
    todo = Todo(**data)
    assert todo.id == id
    assert todo.uid == uid
    assert todo.content == content


def test_todo_model_to_dict():
    uid = str(uuid.uuid4())
    id = str(uuid.uuid4())
    content = 'content'
    data = {
        'id': id,
        'uid': uid,
        'content': content,
    }
    todo = Todo(**data)
    todo_dict = todo.dict()
    assert todo_dict['id'] == id
    assert todo_dict['uid'] == uid
    assert todo_dict['content'] == content


def test_todo_model_comparison():
    uid = str(uuid.uuid4())
    id = str(uuid.uuid4())
    content = 'test'
    data = {
        'id': id,
        'uid': uid,
        'content': content,
    }
    todo1 = Todo(**data)
    todo2 = Todo(**data)
    assert todo1 == todo2


def test_todo_model_should_fail_on_missing_id():
    with pytest.raises(ValueError):
        todo = Todo(content="test", uid='test')


def test_todo_model_should_fail_on_missing_uid():
    with pytest.raises(ValueError):
        todo = Todo(content="test", id='test')


def test_user_model_should_fail_on_missing_content():
    with pytest.raises(ValueError):
        todo = Todo(uid="test", id='test')
