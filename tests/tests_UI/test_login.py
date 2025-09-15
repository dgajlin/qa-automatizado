import pytest
from faker import Faker
from pages.UI.signup_page import SignupPage

faker = Faker()

@pytest.mark.login
def test_login(logged_in):
    # Si la fixture no lanza excepcion implica que el login fue exitoso
    assert True

@pytest.mark.parametrize("firstname, lastname, email, zipcode, password",
    [
        (faker.first_name(), faker.last_name(), faker.unique.email(), faker.postcode(), faker.password()),
        ("", faker.last_name(), faker.unique.email(), faker.postcode(), faker.password()),
    ],
)
@pytest.mark.login
def test_signup(driver, homepage, firstname, lastname, email, zipcode, password):
    # Registro de nuevo usuario
    homepage.go_to_signup()
    signup = SignupPage(driver)
    signup.signup(firstname, lastname, email, zipcode, password)
