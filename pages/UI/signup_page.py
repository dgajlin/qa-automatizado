from pages.UI.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class SignupPage(BasePage):

    INPUT_FIRSTNAME = (By.ID, "firstName")
    INPUT_LASTNAME = (By.ID, "lastName")
    INPUT_EMAIL = (By.ID, "email")
    INPUT_ZIPCODE = (By.ID, "zipCode")
    INPUT_PASSWORD = (By.ID, "password")
    BUTTON_SIGNUP = (By.CSS_SELECTOR, "button[type='submit']")
    TEXT_SIGNUP = (By.XPATH, "//h1[normalize-space()='Signup Successful']")

    def signup(self, firstname, lastname, email, zipcode, password):
        self.type(self.INPUT_FIRSTNAME, firstname)
        self.type(self.INPUT_LASTNAME, lastname)
        self.type(self.INPUT_EMAIL, email)
        self.type(self.INPUT_ZIPCODE, zipcode)
        self.type(self.INPUT_PASSWORD, password)
        self.click(self.BUTTON_SIGNUP)
        try:
            return "Signup Successful" in self.text_of_element(self.TEXT_SIGNUP)
        except TimeoutException:
            return False