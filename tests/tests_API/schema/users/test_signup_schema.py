import pytest
from faker import Faker
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

faker = Faker()

signup_schema = {
    "type": "object",
    "required": ["email", "password", "full_name"],
    "properties": {
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string", "minLength": 6},
        "full_name": {"type": "string", "minLength": 1},
    },
    "additionalProperties": False
}

validator = Draft202012Validator(signup_schema, format_checker=FormatChecker())

@pytest.mark.parametrize("email, password, full_name, expected",
    [
        (faker.email(), faker.password(length=10, special_chars=False), faker.name(), True),  # formato de datos valido
        ("no-email", faker.password(length=10, special_chars=False), faker.name(), False),    # password con formato invalido (minLength>=6)
        ("", faker.password(length=10, special_chars=False), faker.name(), False),            # usuario no ingresado
        (faker.unique.email(), "", faker.name(), False),                                      # password no ingresada
        (faker.unique.email(), faker.password(length=10, special_chars=False), "", False),    # full_name no ingresado
        ("", "", faker.name(), False),                                                        # usuario y password no ingresados
        ("", "", "", False),                                                                  # usuario, password y full_name no ingresados
    ],
)
@pytest.mark.schema
def test_signup_schema(email, password, full_name, expected):
    data = {"email": email, "password": password, "full_name": full_name}
    try:
        validator.validate(data)
        valid = True
    except ValidationError:
        valid = False
    assert valid is expected
