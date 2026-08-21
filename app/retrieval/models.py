from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedCodeChunk:
    content: str
    file_path: str
    language: str
    symbol: str
    symbol_type: str
    start_line: int
    end_line: int
    distance: float