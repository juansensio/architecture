from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.application.user.RegisterUser import RegisterUser
from src.application.user.RetrieveUser import RetrieveUser
from src.application.todo.CreateTodo import CreateTodo
from src.application.todo.RetrieveTodos import RetrieveTodos
from src.application.todo.UpdateTodo import UpdateTodo
from src.application.todo.DeleteTodo import DeleteTodo

# from src.infrastructure.user.UserFirebaseRepo import UserFirebaseRepo as UserRepository
from src.infrastructure.user.UserMemRepo import UserMemRepo as UserRepository
from src.infrastructure.todo.TodoMemRepo import TodoMemRepo as TodoRepository

app = FastAPI()


@app.get("/users/register")
async def register_user(username: str, password: str):
    try:
        repo = UserRepository()
        register_user = RegisterUser(repo)
        inputs = RegisterUser.Inputs(username=username, password=password)
        result = register_user(inputs)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        repo = UserRepository()
        retrieve_user = RetrieveUser(repo)
        inputs = RetrieveUser.Inputs(
            username=form_data.username, password=form_data.password)
        result = retrieve_user(inputs)
        return {"access_token": result.user.uid, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    uid = token
    if not uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return uid


class CreateTodoBody(BaseModel):
    content: str


@app.post("/todos")
async def create_todo(body: CreateTodoBody, uid: str = Depends(get_current_user)):
    try:
        repo = TodoRepository()
        user_repo = UserRepository()
        create_todo = CreateTodo(repo, user_repo)
        inputs = CreateTodo.Inputs(uid=uid, content=body.content)
        return create_todo(inputs)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/todos")
async def retrieve_todos(uid: str = Depends(get_current_user)):
    try:
        repo = TodoRepository()
        user_repo = UserRepository()
        retrieve_todos = RetrieveTodos(repo, user_repo)
        inputs = RetrieveTodos.Inputs(uid=uid)
        return retrieve_todos(inputs).todos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class UpdateTodoBody(BaseModel):
    content: str


@app.put("/todos/{id}")
async def update_todo(id: str, body: UpdateTodoBody, uid: str = Depends(get_current_user)):
    try:
        repo = TodoRepository()
        update_todo = UpdateTodo(repo)
        inputs = UpdateTodo.Inputs(id=id, new_content=body.content)
        todo = update_todo(inputs).todo
        return {
            "id": todo.id,
            "content": todo.content,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/todos/{id}")
async def update_todo(id: str, uid: str = Depends(get_current_user)):
    try:
        repo = TodoRepository()
        user_repo = UserRepository()
        delete_todo = DeleteTodo(repo, user_repo)
        inputs = DeleteTodo.Inputs(uid=uid, id=id)
        return delete_todo(inputs)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
