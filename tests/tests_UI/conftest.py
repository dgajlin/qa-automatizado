import pytest
import os
from utils.settings import WEB_BASE_URL_UI, USER_LOGIN_UI, USER_PASSWORD_UI
from utils.driver_factory import create_driver
from pages.UI.home_page import HomePage
from pages.UI.product_page import ProductPage
from pages.UI.finish_page import FinishPage
from pages.UI.checkout_page import CheckoutPage
from pages.UI.cart_page import CartPage
from pages.UI.login_page import LoginPage

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=os.getenv("HEADLESS", "1"),
        help="Ejecutar pruebas en modo headless (sin interfaz de usuario)"
    )
    parser.addoption(
        "--mybrowser",
        action="store",
        default=os.getenv("BROWSER", "chrome"),
        help="Navegador a utilizar: chrome, firefox o edge"
    )

@pytest.fixture
def driver(request):
    headless_option = request.config.getoption("--headless")
    headless = str(headless_option).lower() == "1"
    browser = request.config.getoption("--mybrowser").lower()
    driver = create_driver(browser, headless=headless)
    yield driver
    driver.quit()

@pytest.fixture
def base_url_shop():
    return WEB_BASE_URL_UI

@pytest.fixture
def homepage(driver, base_url_shop):
    page = HomePage(driver)
    page.load()
    return page

@pytest.fixture
def logged_in(driver, homepage):
    homepage.go_to_login()
    login = LoginPage(driver)
    login.login(USER_LOGIN_UI, USER_PASSWORD_UI)
    return login

@pytest.fixture
def product_factory(driver, homepage):
    def _add_product(category_id, product_id):
        homepage.open_category(category_id)
        product = ProductPage(driver)
        product.add_to_cart(product_id)
        return product
    return _add_product

@pytest.fixture
def checkout_page(driver):
    return CheckoutPage(driver)

@pytest.fixture
def finish_page(driver):
    return FinishPage(driver)

@pytest.fixture
def cart_page(driver):
    return CartPage(driver)