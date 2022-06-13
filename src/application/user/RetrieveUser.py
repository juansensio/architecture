from ...domain.user.user import User
from ...domain.user.errors import UserNotFoundError, InvalidCredentialsError
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
        if user['password'] != inputs.password:
            raise InvalidCredentialsError()
        return self.Outputs(user=user)
