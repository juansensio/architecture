import typer
from pathlib import Path
import json

app = typer.Typer()


@app.command()
def register(email: str = typer.Argument(..., help="The email of the user")):
    """
    Register to the TODO app with your email and password.
    """
    typer.echo(f'Hello {email}!')


@app.command()
# def login(
#     email: str = typer.Option(..., help="The email of the user",
#                               prompt='Your email'),
#     password: str = typer.Option(..., help="The password of the user",
#                                  prompt='Your password', confirmation_prompt=True, hide_input=True),
# ):
def login():
    """
    Login to the TODO app with your email and password.
    Your credentials are stored until your run the logout command.
    """
    creds = Path('.creds.json')
    if creds.exists():
        # read json file and get email and password
        with open(creds, 'r') as f:
            creds = json.load(f)
            email = creds['email']
            password = creds['password']
        typer.echo(f'Hello {email}!')
    else:
        email = typer.prompt('Your email')
        password = typer.prompt(
            'Your password', confirmation_prompt=True, hide_input=True)
        # save json file with email and password
        creds.write_text(f'{{"email": "{email}", "password": "{password}"}}')

    # try:
    #     typer.secho(f'Hello {email}!', fg=typer.colors.MAGENTA)
    #     # raise Exception("ei")
    # except Exception as e:
    #     typer.echo(f'error: {e}')
    #     raise typer.Exit(code=1)
    #     # raise typer.Abort()


@app.command()
def logout():
    """
    Logout from the TODO app.
    """
    creds = Path('.creds.json')
    if creds.exists():
        creds.unlink()
    typer.echo('Bye!')


if __name__ == "__main__":
    app()
