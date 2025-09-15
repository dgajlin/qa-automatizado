import pytest
from faker import Faker
from datetime import datetime, timedelta
import random
import string
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

faker = Faker()
now = datetime.now()
extra_minutes = random.randint(30, 180)
past = now - timedelta(minutes=extra_minutes)
future = now + timedelta(minutes=extra_minutes)
current_datetime = now.isoformat() + "Z"
future_datetime = future.isoformat() + "Z"

create_airport_schema = {
    "type": "object",
    "required": ["origin", "destination", "departure_time", "arrival_time", "base_price", "aircraft_id"],
    "properties": {
        "origin": {"type": "string", "pattern": "^[A-Z]{3}$"},
        "destination": {"type": "string", "pattern": "^[A-Z]{3}$"},
        "departure_time": {"type": "string", "format": "date-time"},
        "arrival_time": {"type": "string", "format": "date-time"},
        "base_price": {"type": "number", "minimum": 1},
        "aircraft_id": {"type": "string", "minLength": 1},
    },
    "additionalProperties": False
}

validator = Draft202012Validator(create_airport_schema, format_checker=FormatChecker())

@pytest.mark.parametrize("origin, destination, departure_time, arrival_time, base_price, aircraft_id, expected",
    [
        (faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         current_datetime, future_datetime, 100, "ABCDE", True),                             # formato de datos valido
        (faker.unique.bothify(text="??", letters=string.ascii_uppercase),
         faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         current_datetime, future_datetime, 100, "ABCDE", False),                            # origen con formato invalido (LL)
        (faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         faker.unique.bothify(text="??", letters=string.ascii_uppercase),
         current_datetime, future_datetime, 100, "ABCDE", False),                            # destino con formato invalido (LL)
        ("",faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         current_datetime, future_datetime, 100, "ABCDE", False),                            # origen no ingresado
        (faker.unique.bothify(text="???", letters=string.ascii_uppercase), "",
         current_datetime, future_datetime, 100, "ABCDE", False),                            # destino no ingresado
        (faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         "", future_datetime, 100, "ABCDE", False),                                          # current_datetime no ingresado
        (faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         current_datetime, "", 100, "ABCDE", False),                                         # future_datetime no ingresado
        (faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         current_datetime, future_datetime, 0, "ABCDE", False),                              # base_price no ingresada
        (faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         faker.unique.bothify(text="???", letters=string.ascii_uppercase),
         current_datetime, future_datetime, 100, "", False),                                 # aircraft_id, no ingresado
    ],
)
@pytest.mark.schema
def test_create_schema(origin, destination, departure_time, arrival_time, base_price, aircraft_id, expected):
    data = {"origin": origin, "destination": destination, "departure_time": departure_time, "arrival_time": arrival_time, "base_price": base_price, "aircraft_id": aircraft_id}
    try:
        validator.validate(data)
        valid = True
    except ValidationError:
        valid = False
    assert valid is expected
