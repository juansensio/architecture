from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.application.user.RegisterUser import RegisterUser
# from src.infrastructure.user.UserFirebaseRepo import UserFirebaseRepo as UserRepository
from src.infrastructure.user.UserMemRepo import UserMemRepo as UserRepository

app = FastAPI()


@app.get("/users/register")
async def register_user(username: str, password: str):
    try:
        repo = UserRepository()
        register_user = RegisterUser(repo)
        inputs = RegisterUser.Inputs(username=username, password=password)
        result = register_user(inputs)
        return result.user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
