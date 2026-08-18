import ast

from app.indexing.models import ParsedCode, ParsedSymbol
from app.parsing.code_parser import CodeParser


class PythonASTVisitor(ast.NodeVisitor):

    def __init__(self):
        self.symbols: list[ParsedSymbol] = []
        self.current_class: str | None = None

    def visit_ClassDef(self, node: ast.ClassDef):
        self.symbols.append(
            ParsedSymbol(
                name=node.name,
                symbol_type="class",
                line_start=node.lineno,
                line_end=node.end_lineno,
            )
        )

        previous_class = self.current_class
        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = previous_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        symbol_type = "method" if self.current_class else "function"

        self.symbols.append(
            ParsedSymbol(
                name=node.name,
                symbol_type=symbol_type,
                line_start=node.lineno,
                line_end=node.end_lineno,
                parent=self.current_class,
            )
        )

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        symbol_type = "method" if self.current_class else "function"

        self.symbols.append(
            ParsedSymbol(
                name=node.name,
                symbol_type=symbol_type,
                line_start=node.lineno,
                line_end=node.end_lineno,
                parent=self.current_class,
            )
        )

        self.generic_visit(node)


class PythonCodeParser(CodeParser):

    def parse(self, source_code: str) -> ParsedCode:
        tree = ast.parse(source_code)

        visitor = PythonASTVisitor()
        visitor.visit(tree)

        return ParsedCode(symbols=visitor.symbols)