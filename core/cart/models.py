from django.db import models

from rest_framework.exceptions import APIException
from rest_framework import status

from product.models import Product

from user.models import User


class Cart(models.Model):
    cart_owner = models.ForeignKey(User,
                                   verbose_name='Власник кошику',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=False)

    def clean(self):
        if not self.cart_owner:
            raise APIException("Cart owner must be specified.",
                               code=status.HTTP_400_BAD_REQUEST)

    def __str__(self):
        return f'Cart: {self.id} | Owner: [email: {self.cart_owner.email} - ID: {self.cart_owner.id}]'  # NOQA

    class Meta:
        ordering = ['-id']


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,
                             verbose_name='Кошик',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=False)
    product = models.ForeignKey(Product,
                                verbose_name='Продукт',
                                on_delete=models.CASCADE,
                                null=True,
                                blank=False)
    quantity = models.PositiveIntegerField('Кількість',
                                           default=1,
                                           null=True,
                                           blank=True)

    def clean(self):
        if not self.cart:
            raise APIException("Cart must be specified.",
                               code=status.HTTP_400_BAD_REQUEST)
        if not self.product:
            raise APIException("Product must be specified.",
                               code=status.HTTP_400_BAD_REQUEST)
        if self.quantity <= 0:
            raise APIException("Quantity must be a positive number.",
                               code=status.HTTP_400_BAD_REQUEST)

    def __str__(self):
        _product_title = self.product.title

        if not _product_title.startswith('"'):
            _product_title = f'"{_product_title}'

        if not _product_title.endswith('"'):
            _product_title = f'{_product_title}"'

        return f'{_product_title} | Belongs to cart with ID: {self.cart.id}'

    class Meta:
        ordering = ['-id']
