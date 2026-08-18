from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class RepositoryFile:
    """
    Represents a file discovered inside a repository.
    """

    path: Path
    language: str
    size_bytes: int
    line_count: int

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


@dataclass(frozen=True)
class RepositorySummary:
    """
    Represents aggregated statistics about a repository.
    """

    total_files: int
    total_lines: int
    total_size_bytes: int
    files_by_language: dict[str, int]
    largest_files: list[RepositoryFile]

@dataclass(frozen=True)
class ParsedSymbol:
    name: str
    symbol_type: str
    line_start: int
    line_end: int
    parent: str | None = None


@dataclass
class ParsedCode:
    symbols: list[ParsedSymbol] = field(default_factory=list)