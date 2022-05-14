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
