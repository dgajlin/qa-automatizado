import pytest
from faker import Faker
from utils.settings import WEB_BASE_URL_API, AUTH_LOGIN

faker = Faker()

@pytest.mark.parametrize("username, password, expected",
    [
        ("admin@demo.com", "admin123", 200),                                           # usuario y password validos
        ("admin@demo.com", faker.password(length=10, special_chars=False), 401),       # usuario valido y password invalida
        (faker.unique.email(), "admin123", 401),                                       # usuario invalido y password valida
        (faker.unique.email(), faker.password(length=10, special_chars=False), 401),   # usuario y password invalidos
    ],
)
@pytest.mark.login
def test_login_api(api_request, username, password, expected):
    payload = {"username": username, "password": password}
    r = api_request(
        "POST",
        f"{WEB_BASE_URL_API}{AUTH_LOGIN}",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == expected, f"Se esperaba '{expected}' pero se obtuvo '{r.status_code}'"
