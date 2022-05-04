from src.infrastructure.user.UserFirebaseRepo import UserFirebaseRepo
import pytest
import uuid

from src.infrastructure.shared.FirebaseRepo import init_db

name = 'todos-test'
collection = 'users-test'

user_dicts = [
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


@pytest.fixture(scope='module')
def db():
    # import warnings
    # warnings.filterwarnings("ignore", category=DeprecationWarning)

    db = init_db(name, creds='./infrastructure/shared/firebase.json')
    for d in user_dicts:
        db.collection(collection).add(d)
    yield db
    docs = db.collection(collection).stream()
    for doc in docs:
        doc.reference.delete()


@pytest.fixture
def user():
    return {
        'uid': str(uuid.uuid4()),
        'username': 'test_user3',
        'password': 'test_password3'
    }


# @pytest.mark.filterwarnings("ignore:Call to deprecated")
def test_user_generate_id(db):
    repo = UserFirebaseRepo(name, collection)
    assert repo.generate_id() != None


def test_user_find_one_by_name(db, user):
    repo = UserFirebaseRepo(name, collection)
    assert repo.find_one_by_name(user['username']) == None
    assert repo.find_one_by_name(user_dicts[0]['username']) == user_dicts[0]


def test_user_persists(db, user):
    repo = UserFirebaseRepo(name, collection)
    repo.persist(user)
    assert len(list(db.collection(collection).get())) == 3
    assert len(list(db.collection(collection).where(
        'username', '==', user['username']).get())) == 1
