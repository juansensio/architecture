from ...domain.todo.todo import Todo
from pydantic import BaseModel
from typing import List
from ...domain.todo.errors import TodoNotFoundError


class RetrieveTodos():
    def __init__(self, repo, user_repo):
        self.repo = repo
        self.user_repo = user_repo

    class Inputs(BaseModel):
        uid: str

    class Outputs(BaseModel):
        todos: List[Todo]

    def __call__(self, inputs: Inputs) -> Outputs:
        todo_ids = self.user_repo.retrieve(inputs.uid)['todos']
        todos = []
        for todo_id in todo_ids:
            if not self.repo.exists(todo_id):
                raise TodoNotFoundError()
            data = self.repo.retrieve(todo_id)
            todos.append(Todo(**data))
        return self.Outputs(todos=todos)
