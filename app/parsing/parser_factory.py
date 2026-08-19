from app.parsing.code_parser import CodeParser
from app.parsing.python_parser import PythonCodeParser


class CodeParserFactory:

    @staticmethod
    def create(language: str | None) -> CodeParser | None:
        if language and language.lower() == "python":
            return PythonCodeParser()

        return None