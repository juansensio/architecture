from src.application.user.RegisterUser import RegisterUser
from src.infrastructure.user.UserFirebaseRepo import UserFirebaseRepo
import pytest
import uuid

from src.domain.user.errors import UserAlreadyExistsError
from src.infrastructure.shared.FirebaseRepo import init_db

name = 'todos-test'
collection = 'users-test'


@pytest.fixture(scope='module')
def db():
    # import warnings
    # warnings.filterwarnings("ignore", category=DeprecationWarning)

    db = init_db(name)
    db.collection(collection).add({
        'uid': str(uuid.uuid4()),
        'username': 'test_user',
        'password': 'test_password'
    })
    db.collection(collection).add({
        'uid': str(uuid.uuid4()),
        'username': 'test_user2',
        'password': 'test_password2'
    })
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


def test_user_persists(db, user):
    repo = UserFirebaseRepo(name, collection)
    register_user = RegisterUser(repo)
    inputs = RegisterUser.Inputs(user=user)
    result = register_user(inputs)
    assert result.user == user
    col = db.collection(collection)
    assert len(list(col.get())) == 3
    assert len(list(col.where('username', "==", user['username']).get())) == 1


def test_should_fail_if_user_exists(db):
    repo = UserFirebaseRepo(name, collection)
    user = {
        'uid': str(uuid.uuid4()),
        'username': 'test_user',
        'password': 'test_password'
    }
    register_user = RegisterUser(repo)
    inputs = RegisterUser.Inputs(user=user)
    with pytest.raises(UserAlreadyExistsError):
        result = register_user(inputs)
