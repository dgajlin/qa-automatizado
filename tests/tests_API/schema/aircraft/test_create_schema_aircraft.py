import pytest
from faker import Faker
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

faker = Faker()

create_aircraft_schema = {
    "type": "object",
    "required": ["tail_number", "model", "capacity"],
    "properties": {
        "tail_number": {"type": "string", "pattern": "^[A-Z]{1,2}-?[A-Z0-9]{2,5}$"},
        "model": {"type": "string", "minLength": 1},
        "capacity": {"type": "integer", "minimum": 1},
    },
    "additionalProperties": False
}

validator = Draft202012Validator(create_aircraft_schema, format_checker=FormatChecker())

@pytest.mark.parametrize("tail_number, model, capacity, expected",
    [
        ("LV-FNK", "Airbus A320", 96, True),            # formato de datos valido
        ("LV-F", "Boeing 737", 101, False),             # tail_number con formato invalido
        ("LV-FNK", "", 100, False),                     # modelo no ingresado
        ("LV-FNK", "Boeing 747", 0, False),             # capacidad no ingresada
        ("", "Airbus A320", 96, False),                 # tail_number no ingresado
    ],
)
@pytest.mark.schema
def test_create_schema(tail_number, model, capacity, expected):
    data = {"tail_number": tail_number, "model": model, "capacity": capacity}
    try:
        validator.validate(data)
        valid = True
    except ValidationError:
        valid = False
    assert valid is expected
