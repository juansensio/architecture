from src.infrastructure.todo.TodoFirebaseRepo import TodoFirebaseRepo
from src.domain.todo.todo import Todo
import pytest
import uuid

from src.infrastructure.shared.FirebaseRepo import init_db

name = 'todos-test'
collection = 'todos-test'

todos_dicts = [
    {
        'uid': str(uuid.uuid4()),
        'id': str(uuid.uuid4()),
        'content': 'test content',

    },
    {
        'uid': str(uuid.uuid4()),
        'id': str(uuid.uuid4()),
        'content': 'test content 2',
    }
]


@pytest.fixture(scope='module')
def db():
    # import warnings
    # warnings.filterwarnings("ignore", category=DeprecationWarning)

    db = init_db(name, creds='./infrastructure/shared/firebase.json')
    for d in todos_dicts:
        doc = db.collection(collection).document()
        doc.set(d)
        d['uid'] = doc.id
    yield db
    docs = db.collection(collection).stream()
    for doc in docs:
        doc.reference.delete()


@pytest.fixture
def todo():
    return {
        'uid': str(uuid.uuid4()),
        'id': str(uuid.uuid4()),
        'content': 'test content 3',
    }


# @pytest.mark.filterwarnings("ignore:Call to deprecated")
def test_todo_generate_id(db):
    repo = TodoFirebaseRepo(name, collection)
    assert repo.generate_id() != None


# def test_user_find_one_by_name(db, user):
#     repo = UserFirebaseRepo(name, collection)
#     assert repo.find_one_by_name(user['username']) == None
#     print(repo.find_one_by_name(user_dicts[0]['username']))
#     # assert repo.find_one_by_name(
#     #     user_dicts[0]['username']) == User(**user_dicts[0])


# def test_user_persists(db, user):
#     repo = UserFirebaseRepo(name, collection)
#     repo.persist(user)
#     assert len(list(db.collection(collection).get())) == 3
#     assert len(list(db.collection(collection).where(
#         'username', '==', user['username']).get())) == 1


# def test_add_todo(db, todo):
#     repo = UserFirebaseRepo(name, collection)
#     uid = user_dicts[0]['uid']
#     repo.add_todo(uid, todo['id'])
#     user_data = db.collection(collection).document(uid).get().to_dict()
#     assert len(user_data['todos']) == 1
#     assert user_data['todos'][0] == todo['id']
