from typer.testing import CliRunner
from utils.creds import Creds, CredentialsNotFound
from main import app
from unittest.mock import patch

runner = CliRunner()


@patch.object(Creds, 'get_username')
def test_login_with_creds(mock_creds):
    username = 'test'
    mock_creds.return_value = username
    result = runner.invoke(app, ["login"])
    assert result.exit_code == 0
    assert f"Hello {username}" in result.stdout


@patch.object(Creds, 'get_username')
def test_login_without_creds(mock_creds):
    mock_creds.side_effect = CredentialsNotFound()
    result = runner.invoke(app, ["login"], inputs=[
                           "test\n", "test\n", "test\n"])
    assert result.exit_code == 1
    # assert 'User not found' in result.stdout
