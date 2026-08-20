from dataclasses import dataclass


@dataclass
class CodeChunk:
    content: str
    file_path: str
    language: str
    symbol: str
    symbol_type: str
    start_line: int
    end_line: int