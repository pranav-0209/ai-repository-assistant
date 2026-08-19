from pathlib import Path

from app.parsing.tree_sitter_code_parser import (
    TreeSitterCodeParser,
)


def test_java_parser_extracts_classes_methods_constructor_and_imports():
    source_path = Path("tests/fixtures/UserService.java")

    source_code = source_path.read_text(
        encoding="utf-8"
    )

    parser = TreeSitterCodeParser()

    result = parser.parse(source_code)

    imports = [
        symbol
        for symbol in result.symbols
        if symbol.symbol_type == "import"
    ]

    classes = [
        symbol
        for symbol in result.symbols
        if symbol.symbol_type == "class"
    ]

    constructors = [
        symbol
        for symbol in result.symbols
        if symbol.symbol_type == "constructor"
    ]

    methods = [
        symbol
        for symbol in result.symbols
        if symbol.symbol_type == "method"
    ]

    assert len(imports) == 2
    assert {
        symbol.name
        for symbol in imports
    } == {
        "repositories.UserRepository",
        "java.util.List",
    }

    assert len(classes) == 1
    assert classes[0].name == "UserService"

    assert len(constructors) == 1
    assert constructors[0].name == "UserService"
    assert constructors[0].parent == "UserService"

    assert len(methods) == 1
    assert methods[0].name == "createUser"
    assert methods[0].parent == "UserService"