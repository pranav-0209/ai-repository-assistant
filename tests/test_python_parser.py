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


def test_python_parser_extracts_imports():
    source_code = """
import jwt
import numpy as np

from repositories.user import UserRepository
from utils.security import hash_password as hash
"""

    parser = PythonCodeParser()

    result = parser.parse(source_code)

    imports = [
        symbol
        for symbol in result.symbols
        if symbol.symbol_type == "import"
    ]

    assert len(imports) == 4

    assert imports[0].name == "jwt"
    assert imports[1].name == "numpy as np"
    assert imports[2].name == "repositories.user.UserRepository"
    assert imports[3].name == "utils.security.hash_password as hash"