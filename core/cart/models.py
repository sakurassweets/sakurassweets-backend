from django.db import models

from product.models import Product

from user.models import User


class Cart(models.Model):
    cart_owner = models.ForeignKey(User,
                                   verbose_name='Власник кошику',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=False)

    def __str__(self):
        return f'Cart: {self.id} | Owner: [email: {self.cart_owner.email} - ID: {self.cart_owner.id}]'  # NOQA

    class Meta:
        ordering = ['-id']


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,
                             verbose_name='Кошик',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    product = models.ForeignKey(Product,
                                verbose_name='Продукт',
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    quantity = models.PositiveIntegerField('Кількість',
                                           default=1,
                                           null=True,
                                           blank=True)

    def __str__(self):
        _product_title = self.product.title

        if not _product_title.startswith('"'):
            _product_title = f'"{_product_title}'

        if not _product_title.endswith('"'):
            _product_title = f'{_product_title}"'

        return f'{_product_title} | Belongs to cart with ID: {self.cart.id}'

    class Meta:
        ordering = ['-id']
