import pytest
# Page Objects
from pages.UI.category_page import CategoryPage

@pytest.mark.parametrize("category",
    [
        ("Electronics"),
        ("Groceries"),
        ("Books"),
    ],
)
@pytest.mark.navigation
def test_navigation(driver, homepage, category):
    homepage.select_category(category)
    category_page = CategoryPage(driver)
    title = category_page.get_title()
    assert title == category, f"Título esperado '{category}', obtenido '{title}'"