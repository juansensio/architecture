from typer.testing import CliRunner

from main import app

runner = CliRunner()


def test_login():
    result = runner.invoke(app, ["login"], input="test@example.com\n")
    assert result.exit_code == 0
    assert "Hello test@example.com" in result.stdout
