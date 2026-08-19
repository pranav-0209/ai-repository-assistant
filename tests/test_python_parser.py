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


def test_python_parser_extracts_inheritance():
    source_code = """
class User:
    pass


class AdminUser(User):
    pass
"""

    parser = PythonCodeParser()

    result = parser.parse(source_code)

    assert len(result.inheritances) == 1

    inheritance = result.inheritances[0]

    assert inheritance.child == "AdminUser"
    assert inheritance.parent == "User"

def test_python_parser_extracts_decorators():
    source_code = """
class UserService:

    @staticmethod
    def validate_token(token):
        pass

    @router.get("/users")
    def get_users(self):
        pass
"""

    parser = PythonCodeParser()

    result = parser.parse(source_code)

    validate_token = result.symbols[1]
    get_users = result.symbols[2]

    assert validate_token.name == "validate_token"
    assert validate_token.decorators[0].name == "staticmethod"
    assert validate_token.decorators[0].arguments is None

    assert get_users.name == "get_users"
    assert get_users.decorators[0].name == "router.get"
    assert get_users.decorators[0].arguments == "'/users'"