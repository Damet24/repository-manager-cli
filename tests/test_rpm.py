# tests/test_rpm.py


from typer.testing import CliRunner

from rpm import __app_name__, __version__, cli

runner = CliRunner()

def test_version_cli():
    result = runner.invoke(cli.app, ["--version"])
    print(result.stdout)

    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout
