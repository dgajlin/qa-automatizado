import pytest
from faker import Faker
# Page Objects
from pages.UI.login_page import LoginPage
from pages.UI.signup_page import SignupPage

faker = Faker()

@pytest.mark.parametrize("email, password, expected", [
    (faker.unique.email(), faker.password(), True),   # credenciales válidas
    # password muy larga (5000 caracteres) - Se asume que el backend deberia rechazarla
    (faker.unique.email(), "X" * 5000, False),
    ("", faker.password(), False),                    # email no ingreado
    (faker.unique.email(), "", False),                # password no ingresada
])
@pytest.mark.login
def test_login(driver, homepage, email, password, expected):
    # Prueba de login de usuario
    homepage.go_to_login()
    login = LoginPage(driver)
    result = login.login(email, password)
    assert result == expected, "Login failed"

@pytest.mark.parametrize("firstname, lastname, email, zipcode, password, expected",
    [
        (faker.first_name(), faker.last_name(), faker.unique.email(), faker.postcode(), faker.password(), True),
        # password muy larga (5000 caracteres) - Se asume que el backend deberia rechazarlo
        (faker.first_name(), faker.last_name(), faker.unique.email(), faker.postcode(), "X" * 5000, False),
        ("", faker.last_name(), faker.unique.email(), faker.postcode(), faker.password(), False),
        (faker.first_name(), "", faker.unique.email(), faker.postcode(), faker.password(), False),
        (faker.first_name(), faker.last_name(), "", faker.postcode(), faker.password(), False),
        (faker.first_name(), faker.last_name(), faker.unique.email(), "", faker.password(), False),
        (faker.first_name(), faker.last_name(), faker.unique.email(), faker.postcode(), "", False),
    ],
)
@pytest.mark.login
def test_signup(driver, homepage, firstname, lastname, email, zipcode, password, expected):
    # Prueba de registro de nuevo usuario
    homepage.go_to_signup()
    signup = SignupPage(driver)
    result = signup.signup(firstname, lastname, email, zipcode, password)
    assert result == expected, "Signup failed"
