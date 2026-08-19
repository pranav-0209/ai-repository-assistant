from tree_sitter import Language, Parser
import tree_sitter_java

from app.indexing.models import ParsedCode
from app.parsing.code_parser import CodeParser
from app.parsing.java_tree_sitter_visitor import (
    JavaTreeSitterVisitor,
)


JAVA_LANGUAGE = Language(tree_sitter_java.language())


class TreeSitterCodeParser(CodeParser):

    def __init__(self):
        self.parser = Parser(JAVA_LANGUAGE)

    def parse(self, source_code: str) -> ParsedCode:
        tree = self.parser.parse(
            source_code.encode("utf-8")
        )

        visitor = JavaTreeSitterVisitor(source_code)

        visitor.visit(tree.root_node)

        return visitor.build_result()