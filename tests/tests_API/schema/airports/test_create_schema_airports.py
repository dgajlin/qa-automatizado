import pytest
from faker import Faker
import string
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

faker = Faker()

create_airport_schema = {
    "type": "object",
    "required": ["iata_code", "city", "country"],
    "properties": {
        "iata_code": {"type": "string", "pattern": "^[A-Z]{3}$"},
        "city": {"type": "string", "minLength": 1},
        "country": {"type": "string", "minLength": 1},
    },
    "additionalProperties": False
}

validator = Draft202012Validator(create_airport_schema, format_checker=FormatChecker())

@pytest.mark.parametrize("iata_code, city, country, expected",
    [
        (faker.unique.bothify(text="???", letters=string.ascii_uppercase), faker.city(), faker.country(), True),   # formato de datos valido
        (faker.unique.bothify(text="??", letters=string.ascii_uppercase), faker.city(), faker.country(), False),   # iata_code con formato invalido (LL)
        (faker.unique.bothify(text="###"), faker.city(), faker.country(), False),                                  # iata_code con formato invalido (NNN)
        ("AB1", faker.city(), faker.country(), False),                                                             # iata_code con formato invalido (LLN)
        ("", faker.city(), faker.country(), False),                                                                # iata_code no ingresado
        (faker.unique.bothify(text="???", letters=string.ascii_uppercase), "", faker.country(), False),            # city no ingresada
        (faker.unique.bothify(text="???", letters=string.ascii_uppercase), faker.city, "", False),                 # country no ingresado
    ],
)
@pytest.mark.schema
def test_create_schema(iata_code, city, country, expected):
    data = {"iata_code": iata_code, "city": city, "country": country}
    try:
        validator.validate(data)
        valid = True
    except ValidationError:
        valid = False
    assert valid is expected
