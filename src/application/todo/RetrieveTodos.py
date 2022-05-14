from ...domain.todo.todo import Todo
from pydantic import BaseModel
from typing import List
from ...domain.todo.errors import TodoNotFoundError


class RetrieveTodos():
    def __init__(self, repo):
        self.repo = repo

    class Inputs(BaseModel):
        ids: List[str]

    class Outputs(BaseModel):
        todos: List[Todo]

    def __call__(self, inputs: Inputs) -> Outputs:
        todos = []
        for todo_id in inputs.ids:
            if not self.repo.exists(todo_id):
                raise TodoNotFoundError()
            data = self.repo.retrieve(todo_id)
            todos.append(Todo(**data))
        return self.Outputs(todos=todos)
