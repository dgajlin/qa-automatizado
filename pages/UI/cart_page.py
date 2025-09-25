from pages.UI.base_page import BasePage
from selenium.webdriver.common.by import By

class CartPage(BasePage):
    BTN_PLUS = (By.CSS_SELECTOR, "button svg.lucide-plus")
    BTN_MINUS = (By.CSS_SELECTOR, "button svg.lucide-minus")
    BTN_REMOVE = (By.XPATH, "//button[normalize-space()='Remove']")
    ITEM_QUANTITY = (By.XPATH, "//div[contains(@class,'rounded-full') and contains(@class,'text-xs')]")
    EMPTY_MESSAGE = (By.XPATH, "//h1[normalize-space(.)='Your Cart is Empty']")

    def increase_quantity(self):
        self.action_click(self.BTN_PLUS)

    def decrease_quantity(self):
        self.action_click(self.BTN_MINUS)

    def get_quantity(self) -> int:
        return int(self.text_of_element(self.ITEM_QUANTITY))

    def is_cart_empty(self) -> bool:
        try:
            return "Your Cart is Empty" in self.text_of_element(self.EMPTY_MESSAGE)
        except Exception:
            return False