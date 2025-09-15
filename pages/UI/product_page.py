from pages.UI.base_page import BasePage
from selenium.webdriver.common.by import By

class ProductPage(BasePage):

    PRODUCT_LAPTOP = (By.ID, "add-to-cart-22")
    GO_TO_CART = CHECKOUT_BTN = (By.XPATH, "//a[@href='/cart']/button")

    def add_to_cart(self):
        self.click(self.PRODUCT_LAPTOP)
        self.click(self.GO_TO_CART)
