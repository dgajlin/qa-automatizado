from pages.UI.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class CartPage(BasePage):

    BTN_PLUS = (By.CSS_SELECTOR, "button svg.lucide-plus")
    BTN_MINUS = (By.CSS_SELECTOR, "button svg.lucide-minus")
    BTN_REMOVE = (By.XPATH, "//button[normalize-space()='Remove']")
    BTN_CHECKOUT = (By.XPATH, "//a[@href='/checkout']/button")
    ITEM_QUANTITY = (By.XPATH, "//div[contains(@class,'rounded-full') and contains(@class,'text-xs')]")
    EMPTY_MESSAGE = (By.XPATH, "//h1[normalize-space(.)='Your Cart is Empty']")
    UNIT_PRICE = (By.XPATH, "//div[contains(@class,'text-right')]/p[@class='font-bold']")
    SUBTOTAL = (By.XPATH, "//span[text()='Subtotal']/following-sibling::span")

    def increase_quantity(self):
        self.action_click(self.BTN_PLUS)

    def decrease_quantity(self):
        self.action_click(self.BTN_MINUS)

    def get_quantity(self):
        return int(self.text_of_element(self.ITEM_QUANTITY))

    def is_cart_empty(self):
        try:
            return "Your Cart is Empty" in self.text_of_element(self.EMPTY_MESSAGE)
        except NoSuchElementException:
            return False

    def get_unit_price(self):
        return self.text_of_element(self.UNIT_PRICE)

    def get_subtotal(self):
        return self.text_of_element(self.SUBTOTAL)

    def go_to_checkout(self):
        self.click(self.BTN_CHECKOUT)