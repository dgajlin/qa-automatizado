from pages.UI.base_page import BasePage
from selenium.webdriver.common.by import By

class FinishPage(BasePage):

    CHECKOUT_BTN = (By.XPATH, "//a[@href='/checkout']/button")

    def checkout(self):
        self.click(self.CHECKOUT_BTN)