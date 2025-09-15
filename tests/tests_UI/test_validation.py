import pytest
import os
from datetime import datetime
from faker import Faker
# Page Objects
from pages.UI.checkout_page import CheckoutPage
from selenium.common.exceptions import UnexpectedAlertPresentException

faker = Faker()

def configure_screenshot():
    # Definicion de la configuracion para capturar las pantallas de error
    path = "screeshots"
    filename = f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    if not os.path.exists(path):
        os.makedirs(path)
    filepath = os.path.join(path, filename)
    return filepath

@pytest.mark.parametrize("locator, expected",
    [
        (CheckoutPage.INPUT_FIRST_NAME, "Enter your first name"),
        (CheckoutPage.INPUT_LAST_NAME, "Enter your last name"),
        (CheckoutPage.INPUT_EMAIL, "Enter your email address"),
        (CheckoutPage.INPUT_PHONE, "Enter your phone number"),
        (CheckoutPage.INPUT_ADDRESS, "Enter your street address"),
        (CheckoutPage.INPUT_CITY, "Enter your city"),
        (CheckoutPage.INPUT_ZIP_CODE, "Enter ZIP code"),
        (CheckoutPage.INPUT_COUNTRY, "Enter your country"),
    ],
)
@pytest.mark.validation
def test_checkout_placeholder(checkout_page: CheckoutPage, locator, expected):
    driver = checkout_page.driver

    # Optencion de la configuracion para los screenshoots
    filepath = configure_screenshot()

    # Definicion de un test para la verificacion del valor del placeholder de cada inputbox
    try:
        placeholder = checkout_page.placeholder_of_element(locator).strip()
        assert placeholder == expected, f"Se esperaba '{expected}' pero se obtuvo '{placeholder}'"
    except AssertionError as err:
        # Guardo el screenshot en caso de fallo
        driver.save_screenshot(filepath)
        raise err

@pytest.mark.parametrize(
    "first_name, last_name, email, phone, street_address, city, postcode, country",
    [
        ("", faker.last_name(), faker.email(), faker.msisdn(), faker.street_address(), faker.city(), faker.postcode(), faker.country()),
        (faker.first_name(), "", faker.email(), faker.msisdn(), faker.street_address(), faker.city(), faker.postcode(), faker.country()),
        (faker.first_name(), faker.last_name(), "", faker.msisdn(), faker.street_address(), faker.city(), faker.postcode(), faker.country()),
        (faker.first_name(), faker.last_name(), faker.email(), "", faker.street_address(), faker.city(), faker.postcode(), faker.country()),
        (faker.first_name(), faker.last_name(), faker.email(), faker.msisdn(), "", faker.city(), faker.postcode(), faker.country()),
        (faker.first_name(), faker.last_name(), faker.email(), faker.msisdn(), faker.street_address(), "", faker.postcode(), faker.country()),
        (faker.first_name(), faker.last_name(), faker.email(), faker.msisdn(), faker.street_address(), faker.city(), "", faker.country()),
        (faker.first_name(), faker.last_name(), faker.email(), faker.msisdn(), faker.street_address(), faker.city(), faker.postcode(), ""),
    ],
)
@pytest.mark.validation
def test_checkout_required_fields_validation(
    checkout_page: CheckoutPage,
    first_name, last_name, email, phone, street_address, city, postcode, country):

    checkout_page.fill_checkout_form(
        first_name, last_name, email, phone, street_address, city, postcode, country
    )

    try:
        checkout_page.click_direct(CheckoutPage.BUTTON_PLACE_ORDER)
    except UnexpectedAlertPresentException as e:
        assert "Please fill in all required fields" in str(e.alert_text)


@pytest.mark.parametrize(
    "first_name, last_name, email, phone, street_address, city, postcode, country, locator, expected_part",
    [
        (faker.first_name(), faker.last_name(), "no-email", faker.msisdn(), faker.street_address(), faker.city(), faker.postalcode(), faker.country(),
         CheckoutPage.INPUT_EMAIL, "@"),  # email inválido
    ],
)
@pytest.mark.validation
def test_checkout_validation_error(
    checkout_page: CheckoutPage, first_name, last_name, email, phone, street_address, city, postcode, country, locator, expected_part):

    # Completar el formulario e iniciar proceso de pago
    checkout_page.fill_checkout_form(first_name, last_name, email, phone, street_address, city, postcode, country)
    checkout_page.click_direct(CheckoutPage.BUTTON_PLACE_ORDER)

    element = checkout_page.driver.find_element(*locator)
    msg = element.get_attribute("validationMessage")

    # Validar que el mensaje contenga lo esperado
    assert expected_part in msg, f"Esperaba que '{expected_part}' esté en '{msg}'"
    print(f"Campo {locator}: {msg}")