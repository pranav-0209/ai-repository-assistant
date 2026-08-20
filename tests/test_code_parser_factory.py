from app.parsing.parser_factory import CodeParserFactory
from app.parsing.python_parser import PythonCodeParser
from app.parsing.tree_sitter_code_parser import TreeSitterCodeParser


def test_factory_returns_python_parser():
    parser = CodeParserFactory.create("Python")

    assert isinstance(parser, PythonCodeParser)


def test_factory_returns_java_parser():
    parser = CodeParserFactory.create("Java")

    assert isinstance(parser, TreeSitterCodeParser)


def test_factory_returns_none_for_unsupported_language():
    parser = CodeParserFactory.create("Ruby")

    assert parser is None