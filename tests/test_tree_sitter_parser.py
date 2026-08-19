from pathlib import Path

from app.parsing.tree_sitter_code_parser import (
    TreeSitterCodeParser,
)


def test_java_parser_extracts_classes_methods_and_constructor():
    source_path = Path("tests/fixtures/UserService.java")

    source_code = source_path.read_text(
        encoding="utf-8"
    )

    parser = TreeSitterCodeParser()

    result = parser.parse(source_code)

    assert len(result.symbols) == 3

    user_service = result.symbols[0]
    constructor = result.symbols[1]
    create_user = result.symbols[2]

    assert user_service.name == "UserService"
    assert user_service.symbol_type == "class"
    assert user_service.parent is None

    assert constructor.name == "UserService"
    assert constructor.symbol_type == "constructor"
    assert constructor.parent == "UserService"

    assert create_user.name == "createUser"
    assert create_user.symbol_type == "method"
    assert create_user.parent == "UserService"