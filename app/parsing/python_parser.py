import ast

from app.indexing.models import (
    ParsedCode,
    ParsedDecorator,
    ParsedInheritance,
    ParsedSymbol,
)
from app.parsing.code_parser import CodeParser


class PythonASTVisitor(ast.NodeVisitor):

    def __init__(self):
        self.symbols: list[ParsedSymbol] = []
        self.inheritances: list[ParsedInheritance] = []
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

        for base in node.bases:
            parent_name = self._extract_expression_name(base)

            if parent_name:
                self.inheritances.append(
                    ParsedInheritance(
                        child=node.name,
                        parent=parent_name,
                    )
                )

        previous_class = self.current_class
        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = previous_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._add_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._add_function(node)
        self.generic_visit(node)

    def _add_function(self, node):
        symbol_type = "method" if self.current_class else "function"

        decorators = tuple(
            decorator
            for decorator in (
                self._extract_decorator(item)
                for item in node.decorator_list
            )
            if decorator is not None
        )

        self.symbols.append(
            ParsedSymbol(
                name=node.name,
                symbol_type=symbol_type,
                line_start=node.lineno,
                line_end=node.end_lineno,
                parent=self.current_class,
                decorators=decorators,
            )
        )

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            import_name = alias.name

            if alias.asname:
                import_name = f"{alias.name} as {alias.asname}"

            self.symbols.append(
                ParsedSymbol(
                    name=import_name,
                    symbol_type="import",
                    line_start=node.lineno,
                    line_end=node.end_lineno,
                )
            )

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module or ""

        for alias in node.names:
            import_name = (
                f"{module}.{alias.name}"
                if module
                else alias.name
            )

            if alias.asname:
                import_name = f"{import_name} as {alias.asname}"

            self.symbols.append(
                ParsedSymbol(
                    name=import_name,
                    symbol_type="import",
                    line_start=node.lineno,
                    line_end=node.end_lineno,
                )
            )

        self.generic_visit(node)

    def _extract_expression_name(self, node):
        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Attribute):
            parent = self._extract_expression_name(node.value)

            if parent:
                return f"{parent}.{node.attr}"

            return node.attr

        return None

    def _extract_decorator(self, node):
        if isinstance(node, ast.Name):
            return ParsedDecorator(
                name=node.id
            )

        if isinstance(node, ast.Attribute):
            name = self._extract_expression_name(node)

            if name:
                return ParsedDecorator(
                    name=name
                )

        if isinstance(node, ast.Call):
            name = self._extract_expression_name(node.func)

            if name:
                arguments = ", ".join(
                    ast.unparse(argument)
                    for argument in node.args
                )

                return ParsedDecorator(
                    name=name,
                    arguments=arguments or None,
                )

        return None


class PythonCodeParser(CodeParser):

    def parse(self, source_code: str) -> ParsedCode:
        tree = ast.parse(source_code)

        visitor = PythonASTVisitor()
        visitor.visit(tree)

        return ParsedCode(
            symbols=visitor.symbols,
            inheritances=visitor.inheritances,
        )