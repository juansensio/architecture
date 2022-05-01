# Documentation

This is a simple documentation for the library.

Running tests:

```
pytest
```

## User

### Model

Pydantic handles field validation, serialization and more...

[domain/user/user.py](../domain/user/user.py)

```python
from pydantic import BaseModel


class User(BaseModel):
    uid: str
    username: str
    password: str
```

### Repositories

Inherit from model-agnostic repository implementations, implement custom functionality

[infrastructure/user/UserMemRepo.py](../infrastructure/user/UserMemRepo.py)

```python
from ..shared.MemRepo import MemRepo


class UserMemRepo(MemRepo):
    def __init__(self, data):
        self.data = data

    def find_one_by_name(self, name):
        return super().find_one_by_name('username', name)
```

### Errors

[domain/user/errors.py](../domain/user/errors.py)

```python
class UserAlreadyExistsError(Exception):
    pass
```

### Use cases

Use cases implement the business logic and communicate with the infrastructure via its inputs/outputs interfaces.

#### User registration

[application/user/register_user.py](../application/user/register_user.py)

```python
from ...domain.user.user import User
from ...domain.user.errors import UserAlreadyExistsError
from pydantic import BaseModel


class RegisterUser():
    def __init__(self, repo):
        self.repo = repo

    class Inputs(BaseModel):
        user: User

    class Outputs(BaseModel):
        user: User

    def __call__(self, inputs: Inputs) -> Outputs:
        if self.repo.find_one_by_name(inputs.user.username):
            raise UserAlreadyExistsError()
        result = self.repo.persist(inputs.user.dict())
        return self.Outputs(user=User(**result))
```

## TODOs

...

## Databases

### Memory database

A simple in-memory database.

[infrastructure/shared/MemRepo.py](../infrastructure/shared/MemRepo.py)

```python
class MemRepo():
    def __init__(self, data):
        self.data = data

    def find_one_by_name(self, field, name):
        try:
            ix = [d[field] for d in self.data].index(name)
            return self.data[ix]
        except:
            return None

    def persist(self, data):
        self.data.append(data)
        return data

```
