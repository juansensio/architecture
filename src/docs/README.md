# Documentation

This is a simple documentation for the library.

Running tests:

```
pytest
```

## User

### Model

Pydantic handles field validation, serialization and more... Tested with unit tests.

[domain/user/user.py](../domain/user/user.py)

```python
from pydantic import BaseModel


class User(BaseModel):
    uid: str
    username: str
    password: str
    todos: List[str]
```

### Use cases

Use cases implement the business logic and communicate with the infrastructure via its inputs/outputs interfaces. Tests with unit tests.

#### User registration

[application/user/RegisterUser.py](../application/user/RegisterUser.py)

```python
from ...domain.user.user import User
from ...domain.user.errors import UserAlreadyExistsError
from pydantic import BaseModel



class RegisterUser():
    def __init__(self, repo):
        self.repo = repo

    class Inputs(BaseModel):
        username: str
        password: str

    class Outputs(BaseModel):
        uid: str
        username: str
        todos: list

    def __call__(self, inputs: Inputs) -> Outputs:
        if self.repo.find_one_by_name(inputs.username):
            raise UserAlreadyExistsError()
        uid = self.repo.generate_id()
        user = User(uid=uid, username=inputs.username,
                    password=inputs.password, todos=[])
        self.repo.persist(user.dict())
        return self.Outputs(uid=user.uid, username=user.username, todos=user.todos)


```

#### User retrieve

[application/user/RetrieveUser.py](../application/user/RetrieveUser.py)

```python
from ...domain.user.user import User
from ...domain.user.errors import UserAlreadyExistsError
from pydantic import BaseModel


class RetrieveUser():
    def __init__(self, repo):
        self.repo = repo

    class Inputs(BaseModel):
        username: str
        password: str

    class Outputs(BaseModel):
        user: User

    def __call__(self, inputs: Inputs) -> Outputs:
        user = self.repo.find_one_by_name(inputs.username)
        if not user:
            raise UserNotFoundError()
        if user.password != inputs.password:
            raise InvalidCredentialsError()
        return self.Outputs(user=user)
```

### Errors

[domain/user/errors.py](../domain/user/errors.py)

```python
class UserAlreadyExistsError(Exception):
    def __init__(self):
        self.message = "User already exists"
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __init__(self):
        self.message = "User not found"
        super().__init__(self.message)


class InvalidCredentialsError(Exception):
    def __init__(self):
        self.message = "Invalid credentials"
        super().__init__(self.message)

```

### Repositories

Inherit from model-agnostic repository implementations, implement custom functionality. Tested with integration tests.

[infrastructure/user/UserMemRepo.py](../infrastructure/user/UserMemRepo.py)

```python
from ..shared.MemRepo import MemRepo


class UserMemRepo(MemRepo):
    def __init__(self, data=[]):
        self.data = data

    def find_one_by_name(self, name, field="username"):
        data = super().find_one_by_name(field, name)
        return User(**data) if data else None

    def add_todo(self, uid, todo_id):
        for user in self.data:
            if user['uid'] == uid:
                user['todos'].append(todo_id)
                break
```

[infrastructure/user/UserFirebaseRepo.py](../infrastructure/user/UserFirebaseRepo.py)

```python
from ..shared.FirebaseRepo import FirebaseRepo
from ...domain.user.user import User


class UserFirebaseRepo(FirebaseRepo):
    def __init__(self, name='todos', collection='users'):
        super().__init__(name)
        self.collection = collection

    def find_one_by_name(self, name):
        data = super().find_one_by_name(self.collection, 'username', name)
        return User(**data) if data else None

    def persist(self, data):
        return super().persist(self.collection, data['uid'], data)

    def add_todo(self, uid, todo_id):
        return super().add_item(self.collection, uid, 'todos', todo_id)
```

## TODOs

### Model

[domain/todo/todo.py](../domain/todo/todo.py)

```py
from pydantic import BaseModel


class Todo(BaseModel):
    uid: str
    content: str
    id: str
```

### Use cases

#### Create TODO

[application/todo/CreateTodo.py](../application/todo/CreateTodo.py)

```py
from ...domain.todo.todo import Todo
from pydantic import BaseModel
from ...domain.user.errors import UserNotFoundError


class CreateTodo():
    def __init__(self, repo, user_repo):
        self.repo = repo
        self.user_repo = user_repo

    class Inputs(BaseModel):
        uid: str
        content: str

    class Outputs(BaseModel):
        id: str
        content: str

    def __call__(self, inputs: Inputs) -> Outputs:
        if not self.user_repo.exists(inputs.uid):
            raise UserNotFoundError()
        id = self.repo.generate_id()
        todo = Todo(uid=inputs.uid, content=inputs.content, id=id)
        self.repo.persist(todo.dict())
        self.user_repo.add_todo(todo.uid, todo.id)
        return self.Outputs(id=id, content=todo.content)

```

### Repositories

[infrastructure/todo/TodoMemRepo.py](../infrastructure/todo/TodoMemRepo.py)

```py
from ..shared.MemRepo import MemRepo


class TodoMemRepo(MemRepo):
    def __init__(self, data=[]):
        self.data = data

```

[infrastructure/todo/TodoFirebaseRepo.py](../infrastructure/todo/TodoFirebaseRepo.py)

```py
from ..shared.FirebaseRepo import FirebaseRepo
from ...domain.user.user import User


class TodoFirebaseRepo(FirebaseRepo):
    def __init__(self, name='todos', collection='users'):
        super().__init__(name)
        self.collection = collection

    def persist(self, data):
        return super().persist(self.collection, data['id'], data)

```

## Databases

### Memory database

A simple in-memory database.

[infrastructure/shared/MemRepo.py](../infrastructure/shared/MemRepo.py)

```python
import uuid


class MemRepo():
    def __init__(self, data):
        self.data = data

    def generate_id(self):
        return str(uuid.uuid4())

    def find_one_by_name(self, field, name):
        try:
            ix = [d[field] for d in self.data].index(name)
            return self.data[ix]
        except:
            return None

    def persist(self, data):
        return self.data.append(data)

    def exists(self, name, field='uid'):
        return self.find_one_by_name(name, field) != None


```

### Firebase

A Firebase database.

[infrastructure/shared/FirebaseRepo.py](../infrastructure/shared/FirebaseRepo.py)

```python
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init_db(name, creds="src/infrastructure/shared/firebase.json"):
    try:
        app = firebase_admin.get_app(name)
    except ValueError:
        cred = credentials.Certificate(creds)
        app = firebase_admin.initialize_app(cred, name=name)
    finally:
        return firestore.client(app)



class FirebaseRepo():
    def __init__(self, name="todos"):
        self.db = init_db(name)

    def generate_id(self):
        return self.db.collection(self.collection).document().id

    def find_one_by_name(self, collection, field, name):
        docs = list(self.db.collection(
            collection).where(field, "==", name).get())
        if len(docs) == 0:
            return None
        return docs[0].to_dict()

    def persist(self, collection, document, data):
        return self.db.collection(collection).document(document).set(data)

    def add_item(self, collection, document, field, item):
        return self.db.collection(collection).document(document).update({
            field: firestore.ArrayUnion([item])
        })

```
