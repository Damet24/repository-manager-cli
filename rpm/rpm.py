"""This module provides the Rpm model-controller."""
# rpm/rpm.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional

from rpm import DB_READ_ERROR, ID_ERROR
from rpm.database import DatabeseHandler

class CurrentRepo(NamedTuple):
    repo: Dict[str, Any]
    error: int

class Repoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabeseHandler(db_path)

    def add(self, name: str, url: str, password: Optional[List[str]]):
        """Add a new rpm the database."""

        if password != None:
            password_text = " ".join(password)
        else:
            password_text = ""

        repo = {
            "Name": name,
            "Url": url,
            "Password": password_text
        }
        read = self._db_handler.read_repos()
        if read.error == DB_READ_ERROR:
            return  CurrentRepo(repo, read.error)
        read.repo_list.append(repo)
        write = self._db_handler.write_repos(read.repo_list)
        return CurrentRepo(repo, write.error)

    def get_repo_list(self) -> List[Dict[str, Any]]:
        """Return the current repo list"""
        read = self._db_handler.read_repos()
        return read.repo_list

    def remove(self, repo_id: int) -> CurrentRepo:
        """Remove a repo from the database using its id or index."""
        read = self._db_handler.read_repos()
        if read.error:
            return CurrentRepo({}, read.error)

        try:
            repo = read.repo_list.pop(repo_id - 1)
        except IndexError:
            return CurrentRepo({}, ID_ERROR)

        write = self._db_handler.write_repos(read.repo_list)
        return CurrentRepo(repo, write.error)

    def remove_all(self):
        """Remove all reos from the database."""
        write = self._db_handler.write_repos([])
        return CurrentRepo({}, write.error)

