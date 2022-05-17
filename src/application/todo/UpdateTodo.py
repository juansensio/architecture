from ...domain.todo.todo import Todo
from pydantic import BaseModel
from ...domain.todo.errors import TodoNotFoundError


class UpdateTodo():
    def __init__(self, repo):
        self.repo = repo

    class Inputs(BaseModel):
        id: str
        new_content: str

    class Outputs(BaseModel):
        todo: Todo

    def __call__(self, inputs: Inputs) -> Outputs:
        if not self.repo.exists(inputs.id):
            raise TodoNotFoundError()
        data = self.repo.retrieve(inputs.id)
        new_todo = Todo(uid=data['uid'], id=inputs.id,
                        content=inputs.new_content)
        self.repo.update(new_todo.dict())
        return self.Outputs(todo=new_todo)
