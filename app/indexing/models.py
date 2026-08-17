from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepositoryFile:
    """
    Represents a file discovered inside a repository.
    """

    path: Path

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def extension(self) -> str:
        return self.path.suffix.lower()


@dataclass
class Repository:
    """
    Represents an indexed repository.
    """

    path: Path
    files: list[RepositoryFile]