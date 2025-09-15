from pages.UI.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.settings import WEB_BASE_URL_UI

class HomePage(BasePage):
    URL = WEB_BASE_URL_UI

    IMG_ELECTRONICS = (By.XPATH, '//img[@alt="Electronics"]/ancestor::a[1]')
    LINK_LOGIN = (By.XPATH, "//a[@href='/login']/button")
    LINK_SIGNUP = (By.XPATH, "//a[@href='/signup']/button")

    def load(self):
        self.visit(self.URL)

    def open_electronics_category(self):
        self.click(self.IMG_ELECTRONICS)

    def go_to_login(self):
        self.click(self.LINK_LOGIN)

    def go_to_signup(self):
        self.click(self.LINK_SIGNUP)