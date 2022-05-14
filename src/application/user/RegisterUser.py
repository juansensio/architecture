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
