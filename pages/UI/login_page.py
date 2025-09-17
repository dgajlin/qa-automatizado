from pages.UI.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class LoginPage(BasePage):

    INPUT_EMAIL = (By.ID, "email")
    INPUT_PASSWORD = (By.ID, "password")
    BUTTON_LOGIN = (By.CSS_SELECTOR, "button[type='submit']")
    TEXT_LOGGED_IN = (By.XPATH, "//h1[normalize-space()='Logged In']")

    def login(self, email, password):
        self.type(self.INPUT_EMAIL, email)
        self.type(self.INPUT_PASSWORD, password)
        self.click(self.BUTTON_LOGIN)
        try:
            return "Logged In" in self.text_of_element(self.TEXT_LOGGED_IN)
        except TimeoutException:
            return False
