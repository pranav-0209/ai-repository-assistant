from app.parsing.python_parser import PythonCodeParser


def test_python_parser_extracts_class_and_function():
    source_code = """
class UserService:

    def create_user(self):
        pass


def helper():
    pass
"""

    parser = PythonCodeParser()

    result = parser.parse(source_code)

    assert len(result.symbols) == 3

    assert result.symbols[0].name == "UserService"
    assert result.symbols[0].symbol_type == "class"

    assert result.symbols[1].name == "create_user"
    assert result.symbols[1].symbol_type == "function"

    assert result.symbols[2].name == "helper"
    assert result.symbols[2].symbol_type == "function"