# Documentation

This is a simple documentation for the library.

Running tests

```
pytest
```

## User

Pydantic handles fields validation, serialization and more...

```
from pydantic import BaseModel


class User(BaseModel):
    uid: str
    username: str
    password: str
```

### User registration

User cases implement business logic and interface with the infrastructure via its inputs/outputs interfaces.

```
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

## Database

### Memory database

A simple in-memory database
