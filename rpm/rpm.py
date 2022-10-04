"""This module provides the Rpm model-controller."""
# rpm/rpm.py

from pathlib import Path
from typing import Any, Dict, NamedTuple

from rpm.database import DatabeseHandler

class CurrentRepo(NamedTuple):
    repo: Dict[str, Any]
    error: int

class Repoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabeseHandler(db_path)
