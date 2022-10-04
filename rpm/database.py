"""This module provides the Rpm database functionality."""
# rpm/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from rpm import DB_WRITE_ERROR, DB_READ_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_rpm.json"
)

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the rpm database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Create the rpm database."""
    try:
        db_path.write_text("[]")  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

class DBResponse(NamedTuple):
    repo_list: List[Dict[str, Any]]
    error: int

class DatabeseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_repos(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)

    def write_repos(self, repo_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(repo_list, db, indent=4)
            return DBResponse(repo_list, SUCCESS)
        except OSError:
            return DBResponse(repo_list, DB_WRITE_ERROR)

