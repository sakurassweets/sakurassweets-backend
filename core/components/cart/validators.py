from typing import Literal

from rest_framework.request import Request

from product.models import Product
from cart.models import Cart
from user.models import User


class CreateCartItemValidator:

    error_messages = {
        "high_quantity": "You can't add %(quantity)s of %(product)s, only %(quantity_in_stock)s left.",
        "already_in_cart": "%(product)s is already in your cart.",
        "cart_exists": "Cart [ID: %(id)s] does not exists.",
        "no_permission": "You can't manage items in this cart."
    }

    def __init__(self, request: Request) -> None:
        self.request = request
        self.cart_id = request.data.get('cart')
        self.product_id = request.data.get('product')
        self.quantity = int(request.data.get('quantity'))

    def validate(self) -> str | Literal[True]:
        """Validates cart item creating.

        You can create cart item only if it quantity >= of product
        quantity in stock

        Returns:
            If fails: String object that contains error that occures.
            If passes: Just returns `True`.
        """
        if isinstance(cart := self._get_cart(), str):
            return cart

        self.cart = cart

        if isinstance(result := self._validate_user_is_cart_owner(), str):
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

    def _validate_user_is_cart_owner(self):
        if not self.request.user.id == self.cart.cart_owner.id:
            return self.error_messages["no_permission"]

        return True

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

    def _get_cart(self) -> str | Literal[True]:
        try:
            return Cart.objects.get(id=self.cart_id)
        except Cart.DoesNotExist:
            return self.error_messages['cart_exists'] % {
                "id": self.cart_id
            }

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


class CreateCartValidator:

    error_messages = {
        "cart_exists": "Cart of user '%(user)s' already exists.",
        "no_cart_owner": "User 'ID: %(id)s' does not exists and can't be assigned as cart owner."
    }

    def __init__(self, request: Request) -> None:
        self.request = request
        self.cart_owner_id = request.data['cart_owner']

    def validate(self):
        self.cart_owner = self.__get_cart_owner_email()
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
        try:
            Cart.objects.get(cart_owner=self.cart_owner_id)
            return self.error_messages['cart_exists'] % {
                "user": self.cart_owner
            }
        except Cart.DoesNotExist:
            return True

    def __get_cart_owner_email(self) -> str | Literal[False]:
        try:
            cart_owner = User.objects.get(id=self.cart_owner_id)
            return cart_owner.email
        except User.DoesNotExist:
            return False


class UpdateCartItemValidator:
    error_messages = {
        "wrong_cart": "You can't move you'r items to another cart.",
        "required_fields": "This field is required."
    }
    REQUIRED_FIELDS = ['product', 'quantity', 'cart']

    def __init__(self, request: Request):
        self.request = request

    def validate(self):
        if self.request.method == "PUT":
            if isinstance(result := self._validate_required_fields(), dict):
                return result

        request_cart = self.request.data.get('cart')

        if not request_cart:
            return True

        if self.request.user.is_staff:
            return True

        try:
            cart = Cart.objects.get(cart_owner=self.request.user)
        except Cart.DoesNotExist:
            return self.error_messages["wrong_cart"]

        if not cart.id == self.request.data.get('cart'):
            return self.error_messages["wrong_cart"]

        return True

    def _validate_required_fields(self) -> dict[str, str] | None:
        errors: dict = {}
        for field in self.REQUIRED_FIELDS:
            if field not in self.request.data:
                errors[field] = self.error_messages["required_fields"]

        return errors if errors else None
