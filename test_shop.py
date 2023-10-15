import pytest
from test_shop.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def second_product():
    return Product("card", 150, "Happy Birthday card", 500)

@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    def test_product_check_quantity(self, product):
        assert product.check_quantity(1000)
        assert product.check_quantity(999)
        assert product.check_quantity(0)
        assert product.check_quantity(-1)
        assert product.check_quantity(1001) == False


    def test_product_buy(self, product):
        product.buy(1)
        assert product.check_quantity(999)
        product.buy(999)
        assert product.check_quantity(0)

    def test_product_buy_more_than_available(self, product):
          with pytest.raises(ValueError, match=r"продуктов не хватает"):
            product.buy(9999)


class TestCart:
    def test_add_product(self, product, cart):
        cart.add_product(product, 1)
        assert product in cart.products
        assert cart.products[product] == 1
        cart.add_product(product, 5)
        assert cart.products[product] == 6

    def test_remove_product(self, product, cart):
        cart.add_product(product, 5)
        cart.remove_product(product, 4)
        assert cart.products[product] == 1
        cart.add_product(product, 5)
        cart.remove_product(product)
        assert product not in cart.products
        cart.add_product(product, 5)
        cart.remove_product(product, 5)
        assert product not in cart.products
        cart.add_product(product, 5)
        cart.remove_product(product, 20)
        assert product not in cart.products

    def test_clear(self, product, cart):
        cart.clear()
        assert product not in cart.products
        cart.add_product(product, 5)
        cart.clear()
        assert product not in cart.products


    def test_get_total_price(self, product, cart, second_product):
        cart.add_product(product, 5)
        assert cart.get_total_price() == product.price*5
        cart.clear()
        cart.add_product(product)
        assert cart.get_total_price() == product.price
        cart.clear()
        cart.add_product(second_product, 20)
        cart.add_product(product, 3)
        assert cart.get_total_price() == product.price * 3 + second_product.price * 20


    def test_buy(self, product, cart):
        cart.add_product(product, 5)
        cart.buy()
        assert product not in cart.products
        assert product.quantity == 995
        cart.add_product(product, 995)
        cart.buy()
        assert product not in cart.products
        assert product.quantity == 0
        with pytest.raises(ValueError):
            cart.add_product(product)
            cart.buy()















