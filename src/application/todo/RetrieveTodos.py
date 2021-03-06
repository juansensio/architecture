from ...domain.todo.todo import Todo
from pydantic import BaseModel
from typing import List
from ...domain.todo.errors import TodoNotFoundError
from ...domain.user.errors import UserNotFoundError


class RetrieveTodos():
    def __init__(self, repo, user_repo):
        self.repo = repo
        self.user_repo = user_repo

    class Inputs(BaseModel):
        uid: str

    class Outputs(BaseModel):
        todos: List[Todo]

    def __call__(self, inputs: Inputs) -> Outputs:
        user_data = self.user_repo.retrieve(inputs.uid)
        if not user_data:
            raise UserNotFoundError()
        todos = []
        for todo_id in user_data['todos']:
            if not self.repo.exists(todo_id):
                raise TodoNotFoundError()
            data = self.repo.retrieve(todo_id)
            todos.append(Todo(**data))
        return self.Outputs(todos=todos)
