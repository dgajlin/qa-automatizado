from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def _wait_for_overlay(self):
        overlays = self.driver.find_elements(By.CSS_SELECTOR, "div.fixed.inset-0.z-50")
        if any(o.is_displayed() for o in overlays):
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
                )
            except Exception:
                print("Error el overlay no desapareció luego del timeout")

    def visit(self, url):
        self.driver.get(url)
        #self._wait_for_overlay()

    def type(self, locator, text):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(text)

    def text_of_element(self, locator):
        return self.driver.find_element(*locator).text

    def placeholder_of_element(self, locator):
        #self._wait_for_overlay()
        return self.driver.find_element(*locator).get_attribute("placeholder")

    def element_is_visible(self, locator):
        #self._wait_for_overlay()
        return self.driver.find_element(*locator).is_displayed()

    def click(self, locator):
        self._wait_for_overlay()
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def click_direct(self, locator):
        element = self.driver.find_element(*locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            pass