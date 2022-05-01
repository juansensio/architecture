from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime
from typing import List
import uuid

# fake database

db = {
    "juan": {
        "username": "juan",
        "password": "123",
        "todos": [{
            "id": '123',
            "content": 'test',
            "createdAt": datetime.now(),
        }]
    }
}

app = FastAPI()

# users section


class User(BaseModel):
    username: str
    password: str
    todos: List[dict] = []


@app.get("/users/register")
async def register_user(username: str, password: str):
    if not username in db:
        user_dict = {"username": username, "password": password}
        db[username] = user_dict
        return User(**user_dict)
    raise HTTPException(status_code=400, detail="user already exists")

# auth section

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token):
    username = token
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    user = User(**user_dict)
    if not form_data.password == user.password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# TODOs section


class Todo(BaseModel):
    id: str = uuid.uuid4()
    content: str = ''
    createdAt: datetime = datetime.now()

# create a new todo item


@app.post("/todos")
async def create_todo(content: str, user: User = Depends(get_current_user)):
    todo = Todo(content=content)
    db[user.username]["todos"].append(todo.dict())
    return todo

# retrieve todos


@app.get("/todos")
async def read_todos(user: User = Depends(get_current_user)):
    return db[user.username]["todos"]

# update a todo item


@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, content: str, user: User = Depends(get_current_user)):
    todo_ix = [t['id'] for t in db[user.username]["todos"]].index(todo_id)
    if todo_ix == -1:
        raise HTTPException(status_code=404, detail="todo not found")
    todo = Todo(**db[user.username]["todos"][todo_ix])
    todo.content = content
    db[user.username]["todos"][todo_ix] = todo.dict()
    return todo

# delete a todo item


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str, user: User = Depends(get_current_user)):
    try:
        todo_ix = [t['id'] for t in db[user.username]["todos"]].index(todo_id)
        db[user.username]["todos"].pop(todo_ix)
        return {'message': 'todo deleted'}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
