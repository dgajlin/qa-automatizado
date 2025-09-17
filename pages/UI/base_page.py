from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def _wait_for_overlay(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
            )
        except Exception:
            pass

    def visit(self, url):
        self.driver.get(url)
        self._wait_for_overlay()

    def type(self, locator, text):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)

    def text_of_element(self, locator):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        return element.text

    def placeholder_of_element(self, locator):
        self._wait_for_overlay()
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        return element.get_attribute("placeholder")

    def click(self, locator, timeout=8):
        self._wait_for_overlay()
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return
        except ElementClickInterceptedException:
            raise

    def click_direct(self, locator):
        element = self.driver.find_element(*locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            pass