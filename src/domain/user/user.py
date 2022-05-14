from pydantic import BaseModel
from typing import List


class User(BaseModel):
    uid: str
    username: str
    password: str
    todos: List[str]
