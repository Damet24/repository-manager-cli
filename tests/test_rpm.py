# tests/test_rpm.py

import json

import pytest
from typer.testing import CliRunner

from rpm import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__, 
    __version__, 
    cli,
    rpm,
)

runner = CliRunner()

def test_version_cli():
    result = runner.invoke(cli.app, ["--version"])

    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.fixture
def mock_json_file(tmp_path):
    repo = [{ "name": "test", "url": "http://github.com/damet24/test", "password": "" }]
    db_file = tmp_path / "repo.json"
    with db_file.open("w") as db:
        json.dump(repo, db, indent=4)
    return db_file

test_data1 = {
    "name": "dotfiles",
    "url": "https://github.com/damet24/dotfiles",
    "password": [""],
    "repo" : {
        "Name": "dotfiles",
        "Url": "https://github.com/damet24/dotfiles",
        "Password" : ""
    }
}

test_data2 = {
    "name": "test",
    "url": "https://azure.coltek.com/ticket/ticket.git",
    "password": ["hute8S_hu83pth-tehuc,h.9ru.h91"],
    "repo" : {
        "Name": "test",
        "Url": "https://azure.coltek.com/ticket/ticket.git",
        "Password": "hute8S_hu83pth-tehuc,h.9ru.h91",
    }
}

test_data3 = {
    "name": "test",
    "url": "https://azure.coltek.com/ticket/ticket.git",
    "password": ["hola", "como", "estas?"],
    "repo" : {
        "Name": "test",
        "Url": "https://azure.coltek.com/ticket/ticket.git",
        "Password": "hola como estas?",
    }
}

@pytest.mark.parametrize(
    "name, url, password, expected",
    [
        pytest.param(
            test_data1["name"],
            test_data1["url"],
            test_data1["password"],
            (test_data1["repo"], SUCCESS),
        ),
        pytest.param(
            test_data2["name"],
            test_data2["url"],
            test_data2["password"],
            (test_data2["repo"], SUCCESS),
        ),
        pytest.param(
            test_data3["name"],
            test_data3["url"],
            test_data3["password"],
            (test_data3["repo"], SUCCESS),
        ),
    ]
)
def test_add(mock_json_file, name, url, password, expected):
    repoer = rpm.Repoer(mock_json_file)
    assert repoer.add(name, url, password) == expected
    read = repoer._db_handler.read_repos()
    assert len(read.repo_list) == 2
