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
    parsed_code: ParsedCode | None = None

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
class ParsedDecorator:
    name: str
    arguments: str | None = None


@dataclass(frozen=True)
class ParsedSymbol:
    name: str
    symbol_type: str
    line_start: int
    line_end: int
    parent: str | None = None
    decorators: tuple[ParsedDecorator, ...] = ()


@dataclass(frozen=True)
class ParsedInheritance:
    child: str
    parent: str


@dataclass
class ParsedCode:
    symbols: list[ParsedSymbol] = field(default_factory=list)
    inheritances: list[ParsedInheritance] = field(default_factory=list)