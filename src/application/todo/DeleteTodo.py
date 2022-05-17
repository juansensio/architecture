from pydantic import BaseModel
from ...domain.todo.errors import TodoNotFoundError


class DeleteTodo():
    def __init__(self, repo, user_repo):
        self.repo = repo
        self.user_repo = user_repo

    class Inputs(BaseModel):
        id: str

    class Outputs(BaseModel):
        message: str

    def __call__(self, inputs: Inputs) -> Outputs:
        if not self.repo.exists(inputs.id):
            raise TodoNotFoundError()
        self.repo.delete(inputs.id)
        self.user_repo.remove_todo(inputs.id)
        return self.Outputs(message="todo deleted")
