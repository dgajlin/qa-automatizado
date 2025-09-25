import pytest
from pages.UI.cart_page import CartPage

@pytest.mark.cart
def test_cart_increase_and_empty(cart_page: CartPage):
    # Agregar una laptop al carrito, incrementar la cantidad y verificar
    cart_page.increase_quantity()
    assert cart_page.get_quantity() == 2, "La cantidad debería ser 2 después de incrementar"
    # Decrementar dos veces el producto para eliminarlo del carrito
    cart_page.decrease_quantity()
    assert cart_page.get_quantity() == 1, "La cantidad debería ser 1 después de decrementar"
    cart_page.decrease_quantity()
    assert cart_page.is_cart_empty(), "El carrito debería estar vacío y mostrar 'Your Cart is Empty'"


@pytest.mark.cart
def test_cart_remove_product(cart_page: CartPage):
    # Eliminar el producto con el boton remove y validar
    cart_page.click(cart_page.BTN_REMOVE)
    assert cart_page.is_cart_empty(), "El carrito debería estar vacío y mostrar 'Your Cart is Empty'"