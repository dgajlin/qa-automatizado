import pytest
from faker import Faker
from pages.UI.login_page import LoginPage
from pages.UI.signup_page import SignupPage

faker = Faker()

@pytest.mark.parametrize("email, password, expected", [
    (faker.unique.email(), faker.password(), True),   # credenciales válidas
    ("", faker.password(), False),                    # email no ingreado
    (faker.unique.email(), "", False),                # password no ingresada
])
@pytest.mark.login
def test_login(driver, homepage, email, password, expected):
    homepage.go_to_login()
    login = LoginPage(driver)
    result = login.login(email, password)
    assert result == expected, "Login failed"

@pytest.mark.parametrize("firstname, lastname, email, zipcode, password, expected",
    [
        (faker.first_name(), faker.last_name(), faker.unique.email(), faker.postcode(), faker.password(), True),
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
