from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class Check:
    line: int
    column: int
    message: str
    identifier: str
    classifier: str
    fixer: Fixer

    def fix(self) -> None:
        pass

    def dump(self) -> dict[str, str | int]:
        return {
            "line": self.line,
            "column": self.column,
            "message": self.message,
            "identifier": self.identifier,
            "classifier": self.classifier,
        }


class CommandLineTool(metaclass=ABCMeta):
    """Base class for all tools."""

    def __init__(self, path: Path) -> None:
        self.path = path

    @property
    @abstractmethod
    def version(self) -> str:
        raise NotImplementedError


class Checker(CommandLineTool, metaclass=ABCMeta):
    def get_checks(self, path: Path) -> list[Check]:
        raise NotImplementedError


class Auditor(CommandLineTool, metaclass=ABCMeta):
    pass


class Fixer(CommandLineTool, metaclass=ABCMeta):
    pass


class ChangeLogger(CommandLineTool, metaclass=ABCMeta):
    pass


class VersionControlSystem(CommandLineTool, metaclass=ABCMeta):
    def get_revision(self) -> str:
        raise NotImplementedError


class FixViewer(CommandLineTool, metaclass=ABCMeta):
    def view_diff(self, path: Path, fix: Check) -> None:
        raise NotImplementedError


class Deployer(CommandLineTool, metaclass=ABCMeta):
    pass


class TypeChecker(CommandLineTool, metaclass=ABCMeta):
    pass
