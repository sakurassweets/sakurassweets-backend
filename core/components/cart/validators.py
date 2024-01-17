from typing import Literal

from django.http.request import HttpRequest

from product.models import Product
from cart.models import Cart
from user.models import User


class CartItemValidator:

    error_messages = {
        "high_quantity": "You can't add %(quantity)s of %(product)s, only %(quantity_in_stock)s left.",
        "already_in_cart": "%(product)s is already in your cart.",
        "cart_exists": "Cart [ID: %(id)s] is not exists."
    }

    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.cart_id = request.POST.get('cart')
        self.product_id = request.POST.get('product')
        self.quantity = int(request.POST.get('quantity'))

    def validate_cart_item_creation(self) -> str | Literal[True]:
        """Validates cart item creation.

        You can create cart item only if it quantity >= of product
        quantity in stock

        Returns:
            If fails: String object that contains error that occures.
            If passes: Just returns `True`.
        """
        if isinstance(result := self._validate_cart_not_exists(), str):
            return result

        product = Product.objects.get(id=self.product_id)
        quantity_in_stock = int(product.quantity_in_stock)
        if quantity_in_stock < self.quantity:
            return self.error_messages['high_quantity'] % {
                "quantity": self.quantity,
                "product": product.title,
                "quantity_in_stock": quantity_in_stock
            }

        return self._validate_item_not_in_cart(product)

    def _validate_item_not_in_cart(self, product: Product) -> str | Literal[True]:
        """Validates that item (product) not in cart.

        Args:
            product: product that are being added to cart,
                `Product` instance.

        Returns:
            If fails: String object that contains error that occures.
            If passes: Just returns `True`.
        """
        products_in_cart = self.__extract_list_of_products_in_cart()

        if product.id in products_in_cart:
            return self.error_messages['already_in_cart'] % {
                "product": product.title
            }

        return True

    def _validate_cart_not_exists(self) -> str | Literal[True]:
        if not Cart.objects.get(id=self.cart_id):
            return self.error_messages['cart_exists'] % {
                "id": self.cart_id
            }
        return True

    def __extract_list_of_products_in_cart(self) -> list[int]:
        """Extracts list of products in cart from cart object.

        Returns:
            list object that contains integer id's of products.
        """
        cart = Cart.objects.get(id=self.cart_id)
        products_in_cart_set = cart.cartitem_set.all()
        products_in_cart_values = products_in_cart_set.values_list('product__id',
                                                                   flat=True)
        products_in_cart_list = list(products_in_cart_values)
        return products_in_cart_list


class CartValidator:

    error_messages = {
        "cart_exists": "Cart of user '%(user)s' already exists.",
        "no_cart_owner": "User 'ID: %(id)s' does not exists and can't be assigned as cart owner."
    }

    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.cart_owner_id = request.data['cart_owner']
        self.cart_owner = self.__get_cart_owner_email()

    def validate_cart_creation(self):
        if isinstance(result := self._validate_cart_owner_exists(), str):
            return result

        if isinstance(result := self._validate_cart_not_exists(), str):
            return result

    def _validate_cart_owner_exists(self):
        if not self.cart_owner:
            return self.error_messages['no_cart_owner'] % {
                "id": self.cart_owner_id
            }

    def _validate_cart_not_exists(self) -> str | Literal[True]:
        if Cart.objects.get(cart_owner=self.cart_owner_id):
            return self.error_messages['cart_exists'] % {
                "user": self.cart_owner
            }
        return True

    def __get_cart_owner_email(self) -> str:
        try:
            cart_owner = User.objects.get(id=self.cart_owner_id)
            return cart_owner.email
        except User.DoesNotExist:
            return False
