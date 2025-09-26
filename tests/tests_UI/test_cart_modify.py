import pytest
from utils.settings import ELECTRONICS_ID, SMARTPHONE_ID, BOOKS_ID, PROGRAMING_BOOK_ID

@pytest.mark.cart
def test_cart_increase_and_empty_product(cart_page, product_factory):
    # Agregar un smartphone al carrito
    product_factory(ELECTRONICS_ID, SMARTPHONE_ID)
    # Incrementar la cantidad en una unidad
    cart_page.increase_quantity()
    assert cart_page.get_quantity() == 2, "La cantidad debería ser 2 después de incrementar"
    # Decrementar la cantidad en una unidad
    cart_page.decrease_quantity()
    assert cart_page.get_quantity() == 1, "La cantidad debería ser 1 después de decrementar"
    # Decrementar nuevamenta la cantidad en una unidad para eliminarlo del carrito
    cart_page.decrease_quantity()
    assert cart_page.is_cart_empty(), "El carrito debería estar vacío y mostrar 'Your Cart is Empty'"

@pytest.mark.cart
def test_cart_remove_product(cart_page, product_factory):
    # Agregar un libro al carrito
    product_factory(BOOKS_ID, PROGRAMING_BOOK_ID)
    # Eliminar el producto con el boton remove y validar
    cart_page.click(cart_page.BTN_REMOVE)
    assert cart_page.is_cart_empty(), "El carrito debería estar vacío y mostrar 'Your Cart is Empty'"