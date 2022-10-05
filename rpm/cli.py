"""This module provides the Rpm."""
# rpm/cli.py

from pathlib import Path
from typing import List, Optional

import typer

from rpm import (
    ERRORS, 
    __app_name__, 
    __version__, 
    config, 
    database,
    rpm
)

app = typer.Typer()

@app.command()
def init(db_path: str = typer.Option(
            str(database.DEFAULT_DB_FILE_PATH),
            "--db-path",
            "-db",
             prompt="repo database location?",
         )) -> None:
    """Initialize the repo database"""
    db_init_error = config.init_app(db_path)
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The repo database is {db_path}", fg=typer.colors.GREEN)

def get_repoer() -> rpm.Repoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
        typer.secho(
            'Config file not found. Please, run "rpm init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    if db_path.exists():
        return rpm.Repoer(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "rpm init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def add(
        name: str = typer.Argument(...),
        url: str = typer.Argument(...),
        password: List[str] = typer.Option("", "--password", "-p")
    ) -> None:
    """Add a new repo."""
    repoer = get_repoer()
    repo, error = repoer.add(name, url, password)
    typer.secho(
        f'{repo["Name"]} {error}'
    )
    if error:
        typer.secho(
            f'Adding rpm failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""repo: "{repo['Name']}" was added """,
            # f"""with priority: {}""",
            fg=typer.colors.GREEN,
        )

@app.command(name="list")
def list_all() -> None:
    """List all repos."""
    repoer = get_repoer()
    repo_list = repoer.get_repo_list()
    if len(repo_list) == 0:
        typer.secho(
            "There are no tasks in the repoo list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nrepo list:\n", fg=typer.colors.BLUE, bold=True)

    typer.secho("-" * 70, fg=typer.colors.BLUE)
    for id, repo in enumerate(repo_list, 1):
        name, url, password = repo.values()
        typer.secho(
            f"Id: \t{id}\n"
            f"Name: \t{name}\n"
            f"Url: \t{url}\n"
            f"Password: \t{password}\n",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * 70, fg=typer.colors.BLUE)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
    ) -> None:
    return
