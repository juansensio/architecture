from pydantic import BaseModel


class Todo(BaseModel):
    uid: str
    content: str
    id: str
