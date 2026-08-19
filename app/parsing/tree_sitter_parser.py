from tree_sitter import Language, Parser
import tree_sitter_java


JAVA_LANGUAGE = Language(tree_sitter_java.language())


class JavaTreeSitterParser:

    def __init__(self):
        self.parser = Parser(JAVA_LANGUAGE)

    def parse(self, source_code: str):
        return self.parser.parse(source_code.encode("utf-8"))