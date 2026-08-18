from abc import ABC, abstractmethod

from app.indexing.models import ParsedCode


class CodeParser(ABC):

    @abstractmethod
    def parse(self, source_code: str) -> ParsedCode:
        pass