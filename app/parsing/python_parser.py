import ast

from app.parsing.code_parser import CodeParser
from app.indexing.models import ParsedCode, ParsedSymbol


class PythonCodeParser(CodeParser):

    def parse(self, source_code: str) -> ParsedCode:
        tree = ast.parse(source_code)

        symbols = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                symbols.append(
                    ParsedSymbol(
                        name=node.name,
                        symbol_type="class",
                        line_start=node.lineno,
                        line_end=node.end_lineno,
                    )
                )

            elif isinstance(node, ast.FunctionDef):
                symbols.append(
                    ParsedSymbol(
                        name=node.name,
                        symbol_type="function",
                        line_start=node.lineno,
                        line_end=node.end_lineno,
                    )
                )

        return ParsedCode(symbols=symbols)