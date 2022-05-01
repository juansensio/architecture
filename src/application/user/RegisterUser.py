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
        self.repo.persist(inputs.user.dict())
        return self.Outputs(user=inputs.user)
