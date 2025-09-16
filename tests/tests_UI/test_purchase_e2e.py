import pytest
from faker import Faker
# Page Objects
from pages.UI.checkout_page import CheckoutPage

faker = Faker()

@pytest.mark.e2e
def test_purchase_product(checkout_page: CheckoutPage):
    # Definicion de un test para la compra de un producto y el pago del mismo (Happy Path)
    checkout_page.fill_checkout_form(
        faker.first_name(), faker.last_name(), faker.unique.email(), faker.msisdn(),
        faker.street_address(), faker.city(), faker.postcode(), faker.country()
    )