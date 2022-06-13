import typer
from pathlib import Path
import json

from src.application.user.RegisterUser import RegisterUser
from src.application.user.RetrieveUser import RetrieveUser
from src.application.todo.CreateTodo import CreateTodo
from src.application.todo.RetrieveTodos import RetrieveTodos
from src.application.todo.UpdateTodo import UpdateTodo
from src.application.todo.DeleteTodo import DeleteTodo

from src.infrastructure.user.UserFirebaseRepo import UserFirebaseRepo as UserRepository
from src.infrastructure.todo.TodoFirebaseRepo import TodoFirebaseRepo as TodoRepository
from utils.creds import Creds

app = typer.Typer()
creds = Creds()


@app.command()
def register(
    username: str = typer.Option(..., help="Your username",
                                 prompt='Your username'),
    password: str = typer.Option(..., help="Your password",
                                 prompt='Your password', confirmation_prompt=True, hide_input=True),
):
    """
    Register to the TODO app with your email and password.
    """
    try:
        repo = UserRepository()
        register_user = RegisterUser(repo)
        inputs = RegisterUser.Inputs(username=username, password=password)
        result = register_user(inputs)
        creds.save(result.uid, result.username)
        typer.echo("You have been registered successfully")
    except Exception as e:
        typer.echo(f'error: {e}')
        raise typer.Abort()


@ app.command()
def login():
    """
    Login to the TODO app with your username and password.
    Your credentials are stored until your run the logout command.
    """
    try:
        username = creds.get_username()
        typer.echo(f'Hello {username}!')
    except:
        username = typer.prompt('Your username')
        password = typer.prompt(
            'Your password', confirmation_prompt=True, hide_input=True)
        try:
            repo = UserRepository()
            retrieve_user = RetrieveUser(repo)
            inputs = RetrieveUser.Inputs(username=username, password=password)
            outputs = retrieve_user(inputs)
            user = outputs.user
            creds.save(user.uid, user.username)
        except Exception as e:
            typer.echo(f'error: {e}')
            raise typer.Abort()


@app.command()
def logout():
    """
    Logout from the TODO app.
    """
    creds.remove()
    typer.echo('Bye!')


@app.command()
def ls():
    """
    List all TODOs.
    """
    try:
        uid = creds.get_uid()
        repo = TodoRepository()
        user_repo = UserRepository()
        retrieve_todos = RetrieveTodos(repo, user_repo)
        inputs = RetrieveTodos.Inputs(uid=uid)
        outputs = retrieve_todos(inputs)
        typer.echo(outputs.todos)
    except Exception as e:
        typer.echo(f'error: {e}')
        raise typer.Abort()


if __name__ == "__main__":
    app()
