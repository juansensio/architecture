from src.infrastructure.user.UserFirebaseRepo import UserFirebaseRepo
from src.domain.user.user import User
import pytest
import uuid

from src.infrastructure.shared.FirebaseRepo import init_db

name = 'todos-test'
collection = 'users-test'

user_dicts = [
    {
        'uid': str(uuid.uuid4()),
        'username': 'test_user',
        'password': 'test_password',
        'todos': [],

    },
    {
        'uid': str(uuid.uuid4()),
        'username': 'test_user2',
        'password': 'test_password2',
        'todos': [],
    }
]


@pytest.fixture(scope='module')
def db():
    # import warnings
    # warnings.filterwarnings("ignore", category=DeprecationWarning)

    db = init_db(name, creds='./infrastructure/shared/firebase.json')
    for d in user_dicts:
        doc = db.collection(collection).document()
        d['uid'] = doc.id
        doc.set(d)
    yield db
    docs = db.collection(collection).stream()
    for doc in docs:
        doc.reference.delete()


@pytest.fixture
def user():
    return {
        'uid': str(uuid.uuid4()),
        'username': 'test_user3',
        'password': 'test_password3',
        'todos': [],
    }


@pytest.fixture
def todo():
    return {
        'uid': str(uuid.uuid4()),
        'id': str(uuid.uuid4()),
        'content': 'test content',
    }


# @pytest.mark.filterwarnings("ignore:Call to deprecated")
def test_user_generate_id(db):
    repo = UserFirebaseRepo(name, collection)
    assert repo.generate_id() != None


def test_user_find_one_by_name(db, user):
    repo = UserFirebaseRepo(name, collection)
    assert repo.find_one_by_name(user['username']) == None
    print(repo.find_one_by_name(user_dicts[0]['username']))
    # assert repo.find_one_by_name(
    #     user_dicts[0]['username']) == User(**user_dicts[0])


def test_user_persists(db, user):
    repo = UserFirebaseRepo(name, collection)
    repo.persist(user)
    assert len(list(db.collection(collection).get())) == 3
    assert len(list(db.collection(collection).where(
        'username', '==', user['username']).get())) == 1


def test_user_retrieve(db):
    repo = UserFirebaseRepo(name, collection)
    data = repo.retrieve(user_dicts[0]['uid'])
    assert data == user_dicts[0]
    data = repo.retrieve('123')
    assert data == None


def test_add_todo(db, todo):
    repo = UserFirebaseRepo(name, collection)
    uid = user_dicts[0]['uid']
    repo.add_todo(uid, todo['id'])
    user_data = db.collection(collection).document(uid).get().to_dict()
    assert len(user_data['todos']) == 1
    assert user_data['todos'][0] == todo['id']
