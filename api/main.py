from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uuid

from src.domain.user.user import User
from src.application.user.RegisterUser import RegisterUser
from src.infrastructure.user.UserFirebaseRepo import UserFirebaseRepo

app = FastAPI()


@app.get("/users/register")
async def register_user(username: str, password: str):
    try:
        repo = UserFirebaseRepo()
        register_user = RegisterUser(repo)
        user = User(uid=str(uuid.uuid4()),
                    username=username, password=password)
        inputs = RegisterUser.Inputs(user=user)
        result = register_user(inputs)
        return result.user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
