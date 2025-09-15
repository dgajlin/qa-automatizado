import pytest
from faker import Faker
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

faker = Faker()

login_schema = {
    "type": "object",
    "required": ["email", "password"],
    "properties": {
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string", "minLength": 6},
    },
    "additionalProperties": False,
}

validator = Draft202012Validator(login_schema, format_checker=FormatChecker())

@pytest.mark.parametrize("email,password,expected", [
    ("no-email", faker.password(length=10, special_chars=False), False),    # usuario (email) con formato invalido
    (faker.unique.email(), "123", False),                                   # password con formato invalido (minLength>=6)
    ("", faker.password(length=10, special_chars=False), False),            # usuario no ingresado, password invalida
    (faker.unique.email(), "", False),                                      # usuario invalido, password no ingresada
    ("admin@demo.com", "", False),                                          # usuario valido, password no ingresada ,
    ("", "admin123", False),                                                # usuario no ingresado password valida
    ("", "", False),                                                        # usuario y password no ingresados
])
@pytest.mark.schema
def test_login_schema(email, password, expected):
    data = {"email": email, "password": password}
    try:
        validator.validate(data)
        valid = True
    except ValidationError:
        valid = False
    assert valid is expected
