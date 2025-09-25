from pages.UI.base_page import BasePage
from selenium.webdriver.common.by import By

class CategoryPage(BasePage):
    CATEGORY_TITLE = (By.XPATH, "//h1[@id='category-title']")
    LAPTOP_LINK = (By.XPATH, "//a[@href='/product/22']")

    def get_title(self):
         return self.driver.find_element(*self.CATEGORY_TITLE).text

    def go_to_laptop(self):
        self.click(self.LAPTOP_LINK)