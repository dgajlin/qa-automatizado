from pages.UI.base_page import BasePage
from selenium.webdriver.common.by import By

class ProductPage(BasePage):

    GO_TO_CART = (By.XPATH, "//a[@href='/cart']/button")

    def add_to_cart(self, product_id: int):
        product_locator = (By.ID, f"add-to-cart-{product_id}")
        self.click(product_locator)
        self.click(self.GO_TO_CART)