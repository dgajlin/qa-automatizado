from pages.UI.base_page import BasePage
from selenium.webdriver.common.by import By

class CheckoutPage(BasePage):

    INPUT_FIRST_NAME = (By.ID, "firstName")
    INPUT_LAST_NAME = (By.ID, "lastName")
    INPUT_EMAIL = (By.ID, "email")
    INPUT_PHONE = (By.ID, "phone")
    INPUT_ADDRESS = (By.ID, "address")
    INPUT_CITY = (By.ID, "city")
    INPUT_ZIP_CODE = (By.ID, "zipCode")
    INPUT_COUNTRY = (By.ID, "country")
    BUTTON_PLACE_ORDER = (By.ID, "place-order-button")

    def fill_checkout_form(self, first_name, last_name, email, phone, address, city, zip_code, country):
        self.type(self.INPUT_FIRST_NAME, first_name)
        self.type(self.INPUT_LAST_NAME, last_name)
        self.type(self.INPUT_EMAIL, email)
        self.type(self.INPUT_PHONE, phone)
        self.type(self.INPUT_ADDRESS, address)
        self.type(self.INPUT_CITY, city)
        self.type(self.INPUT_ZIP_CODE, zip_code)
        self.type(self.INPUT_COUNTRY, country)
        self.click(self.BUTTON_PLACE_ORDER)

