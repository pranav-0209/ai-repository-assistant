from app.indexing.models import ParsedCode, ParsedSymbol


class JavaTreeSitterVisitor:

    def __init__(self, source_code: str):
        self.source_bytes = source_code.encode("utf-8")
        self.symbols: list[ParsedSymbol] = []
        self.inheritances = []
        self.current_class: str | None = None

    def visit(self, node):
        if node.type == "class_declaration":
            self._visit_class(node)
            return

        if node.type == "method_declaration":
            self._visit_method(node)
            return

        if node.type == "constructor_declaration":
            self._visit_constructor(node)
            return

        if node.type == "import_declaration":
            self._visit_import(node)
            return

        for child in node.children:
            self.visit(child)

    def _visit_import(self, node):
        import_text = self._node_text(node)

        import_name = (
            import_text
            .removeprefix("import ")
            .removesuffix(";")
            .strip()
        )

        self.symbols.append(
            ParsedSymbol(
                name=import_name,
                symbol_type="import",
                line_start=node.start_point.row + 1,
                line_end=node.end_point.row + 1,
            )
        )

    def _visit_class(self, node):
        class_name_node = self._find_child_by_type(
            node,
            "identifier",
        )

        if class_name_node is None:
            return

        class_name = self._node_text(class_name_node)

        self.symbols.append(
            ParsedSymbol(
                name=class_name,
                symbol_type="class",
                line_start=node.start_point.row + 1,
                line_end=node.end_point.row + 1,
            )
        )

        previous_class = self.current_class
        self.current_class = class_name

        for child in node.children:
            self.visit(child)

        self.current_class = previous_class

    def _visit_method(self, node):
        name_node = self._find_child_by_type(
            node,
            "identifier",
        )

        if name_node is None:
            return

        method_name = self._node_text(name_node)

        self.symbols.append(
            ParsedSymbol(
                name=method_name,
                symbol_type="method",
                line_start=node.start_point.row + 1,
                line_end=node.end_point.row + 1,
                parent=self.current_class,
            )
        )

    def _visit_constructor(self, node):
        name_node = self._find_child_by_type(
            node,
            "identifier",
        )

        if name_node is None:
            return

        constructor_name = self._node_text(name_node)

        self.symbols.append(
            ParsedSymbol(
                name=constructor_name,
                symbol_type="constructor",
                line_start=node.start_point.row + 1,
                line_end=node.end_point.row + 1,
                parent=self.current_class,
            )
        )

    def _find_child_by_type(self, node, node_type: str):
        for child in node.children:
            if child.type == node_type:
                return child

        return None

    def _node_text(self, node) -> str:
        return self.source_bytes[
            node.start_byte:node.end_byte
        ].decode("utf-8")

    def build_result(self) -> ParsedCode:
        return ParsedCode(
            symbols=self.symbols,
            inheritances=self.inheritances,
        )