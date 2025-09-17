from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def _wait_for_overlay(self, timeout=6):
        try:
            overlays = self.driver.find_elements(By.CSS_SELECTOR, "div.fixed.inset-0.z-50")
            if overlays and any(o.is_displayed() for o in overlays):
                WebDriverWait(self.driver, timeout).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
                )
        except Exception:
            return False
        return True

    def visit(self, url):
        self.driver.get(url)
        self._wait_for_overlay()

    def type(self, locator, text):
        element = WebDriverWait(self.driver, 5).until(
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
        element = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(locator)
        )
        return element.get_attribute("placeholder")

    def element_is_visible(self, locator):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    # def click(self, locator, timeout=10, retries=2):
    #     for attempt in range(retries):
    #         self._wait_for_overlay(timeout)
    #         try:
    #             element = WebDriverWait(self.driver, timeout).until(
    #                 EC.element_to_be_clickable(locator)
    #             )
    #             element.click()
    #             return
    #         except ElementClickInterceptedException:
    #             if attempt == retries - 1:
    #                 raise

    def click(self, locator, timeout=8):
        # esperar que no haya overlay
        WebDriverWait(self.driver, timeout).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
        )
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