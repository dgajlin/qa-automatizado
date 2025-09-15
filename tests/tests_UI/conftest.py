import pytest
import os
from utils.settings import WEB_BASE_URL_UI, USER_LOGIN_UI, USER_PASSWORD_UI
from utils.driver_factory import create_driver
from pages.UI.home_page import HomePage
from pages.UI.product_page import ProductPage
from pages.UI.finish_page import FinishPage
from pages.UI.checkout_page import CheckoutPage
from pages.UI.login_page import LoginPage

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=os.getenv("HEADLESS", "1"),
        help="Ejecutar pruebas en modo headless (sin interfaz de usuario)"
    )

@pytest.fixture
def driver(request):
    headless_option = request.config.getoption("--headless")
    headless = str(headless_option).lower() == "1"
    driver = create_driver(headless=headless)
    yield driver
    driver.quit()

@pytest.fixture
def base_url_shop() -> str:
    return WEB_BASE_URL_UI

@pytest.fixture
def homepage(driver, base_url_shop) -> HomePage:
    page = HomePage(driver)
    page.load()
    return page

@pytest.fixture
def logged_in(driver, homepage) -> LoginPage:
    # Logueo a la pagina
    homepage.go_to_login()
    login = LoginPage(driver)
    login.login(USER_LOGIN_UI, USER_PASSWORD_UI)
    return login

@pytest.fixture
def product_added_to_cart(driver, homepage) -> ProductPage:
    # Ingresar a la categoria Electronics y agregar una Laptop al carrito
    homepage.open_electronics_category()
    product = ProductPage(driver)
    product.add_to_cart()
    return product

@pytest.fixture
def checkout_page(driver, product_added_to_cart) -> CheckoutPage:
    # Desde el carrito navegar a Checkout y devolver CheckoutPage
    finish = FinishPage(driver)
    finish.checkout()
    return CheckoutPage(driver)