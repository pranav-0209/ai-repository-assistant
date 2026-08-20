from app.parsing.code_parser import CodeParser
from app.parsing.python_parser import PythonCodeParser
from app.parsing.tree_sitter_code_parser import TreeSitterCodeParser


class CodeParserFactory:

    @staticmethod
    def create(language: str) -> CodeParser | None:
        normalized_language = language.lower()

        if normalized_language == "python":
            return PythonCodeParser()

        if normalized_language == "java":
            return TreeSitterCodeParser()

        return None
