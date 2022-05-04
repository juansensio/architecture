from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.application.user.RegisterUser import RegisterUser
from src.application.user.RetrieveUser import RetrieveUser

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
        return {"access_token": result.user.username, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
