import pytest
from faker import Faker
from utils.settings import LAPTOP_ID, ELECTRONICS_ID

faker = Faker()

@pytest.mark.e2e
def test_purchase_product(product_factory, finish_page, checkout_page):
    # Agregar producto
    product_factory(ELECTRONICS_ID, LAPTOP_ID)
    # Navegar hacia el checkout
    finish_page.checkout()
    # Completar el formulario de pago
    checkout_page.fill_checkout_form(
        faker.first_name(), faker.last_name(), faker.unique.email(), faker.msisdn(),
        faker.street_address(), faker.city(), faker.postcode(), faker.country()
    )