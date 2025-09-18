import pytest
import string
from faker import Faker
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

faker = Faker()

create_booking_schema = {
    "type": "object",
    "required": ["flight_id", "passengers"],
    "properties": {
        "flight_id": {
            "type": "string",
            "pattern": "^[A-Z]{1,2}-?[A-Z0-9]{2,5}$"
        },
        "passengers": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["full_name", "passport"],
                "properties": {
                    "full_name": {"type": "string", "minLength": 1},
                    "passport": {"type": "string", "minLength": 1},
                    "seat": {"type": "string"}
                },
                "additionalProperties": False
            }
        }
    },
    "additionalProperties": False
}

validator = Draft202012Validator(create_booking_schema, format_checker=FormatChecker())

@pytest.mark.parametrize("flight_id, passengers, expected", [
    # formato valido con un pasajero
    ("LV-FNK", [
        {"full_name": faker.name(), "passport": faker.bothify(text="??######", letters=string.ascii_uppercase), "seat": "12A"}
    ], True),
    # flight_id con formato invalido
    ("LV-F", [
        {"full_name": faker.name(), "passport": faker.bothify(text="??######", letters=string.ascii_uppercase), "seat": "12A"}
    ], False),
    # full_name no ingresado
    ("LV-FNK", [
        {"full_name": "", "passport": faker.bothify(text="??######", letters=string.ascii_uppercase), "seat": "12A"}
    ], False),
    # passport no ingresado
    ("LV-FNK", [
        {"full_name": faker.name(), "passport": "", "seat": "12A"}
    ], False),
    # formato válido con dos pasajeros
    ("LV-FNK", [
        {"full_name": faker.name(), "passport": faker.bothify(text="??######", letters=string.ascii_uppercase), "seat": "12A"},
        {"full_name": faker.name(), "passport": faker.bothify(text="??######", letters=string.ascii_uppercase), "seat": "14C"}
    ], True),
    # dos pasajeros (uno valido y otro invalido)
    ("LV-FNK", [
        {"full_name": faker.name(), "passport": faker.bothify(text="??######", letters=string.ascii_uppercase), "seat": "12A"},
        {"full_name": faker.name(), "seat": "14C"}  # falta passport
    ], False),
    # pasajeros no ingresados
    ("LV-FNK", [], False),
])
@pytest.mark.schema
def test_create_schema(flight_id, passengers, expected):
    data = {
        "flight_id": flight_id,
        "passengers": passengers
    }
    try:
        validator.validate(data)
        valid = True
    except ValidationError:
        valid = False
    assert valid is expected
