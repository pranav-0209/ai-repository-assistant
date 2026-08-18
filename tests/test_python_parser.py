from app.parsing.python_parser import PythonCodeParser


def test_python_parser_extracts_class_and_functions():
    source_code = """
class UserService:

    def create_user(self):
        pass

    def delete_user(self):
        pass


def helper():
    pass
"""

    parser = PythonCodeParser()

    result = parser.parse(source_code)

    assert len(result.symbols) == 4

    user_service = result.symbols[0]
    create_user = result.symbols[1]
    delete_user = result.symbols[2]
    helper = result.symbols[3]

    assert user_service.name == "UserService"
    assert user_service.symbol_type == "class"
    assert user_service.parent is None

    assert create_user.name == "create_user"
    assert create_user.symbol_type == "method"
    assert create_user.parent == "UserService"

    assert delete_user.name == "delete_user"
    assert delete_user.symbol_type == "method"
    assert delete_user.parent == "UserService"

    assert helper.name == "helper"
    assert helper.symbol_type == "function"
    assert helper.parent is None