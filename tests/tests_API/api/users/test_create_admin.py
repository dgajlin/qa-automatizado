import pytest
from time import time
from faker import Faker

faker = Faker()

@pytest.mark.parametrize("username, password, fullname, expected",
    [
        # usuario, password y full_name validos
        (f"{faker.user_name()}{str(int(time()*100))[-6:]}@example.org", faker.password(length=10, special_chars=False), faker.name(), 201),
        # usuario no ingresado
        ("", faker.password(length=10, special_chars=False), faker.name(), 422),
        # password no ingresada
        (f"{faker.user_name()}{str(int(time()*100))[-6:]}@example.org", "", faker.name(), 422),
    ],
)
@pytest.mark.user
def test_create_admin(delete_user, create_admin_user, username, password, fullname, expected):
    r = create_admin_user(username, password, fullname)
    assert r.status_code == expected, f"Se esperaba '{expected}' pero se obtuvo '{r.status_code}'"
    user_id = r.json().get('id')
    delete_user(user_id)


@pytest.mark.user
def test_create_admin_unauthorized(create_admin_user):
    email = f"{faker.user_name()}{str(int(time()*100))[-6:]}@example.org"
    password = faker.password(length=10, special_chars=False)
    fullname = faker.name()
    r = create_admin_user(email, password, fullname, headers=None)
    assert r.status_code == 401, f"Se esperaba 401 pero se obtuvo {r.status_code}"