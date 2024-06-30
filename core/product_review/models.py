from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Avg

from product.models import Product
from user.models import User


def validate_rating(value):
    if value not in [1, 2, 3, 4, 5]:
        raise ValidationError('Rating must be 1, 2, 3, 4, or 5')


class ProductReview(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    product = models.ForeignKey(
        Product, verbose_name='Відноситься до продукту', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, verbose_name='Відноситься до користувача', on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        default=0,
        null=False,
        blank=False,
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(verbose_name='Відгук', null=True, blank=True, max_length=500)

    def save(self, *args, **kwargs):
        super(ProductReview, self).save(*args, **kwargs)
        self.update_product_rating()

    def update_product_rating(self):
        product = self.product
        ratings = ProductReview.objects.filter(product=product)
        avg_product_rating = ratings.aggregate(Avg("rating"))['rating__avg']

        if avg_product_rating is not None:
            product.rating = round(avg_product_rating, 1)  # Round to handle decimal averages
        else:
            product.rating = 0

        product.save()

    def __str__(self):
        return f"{self.user.email} - {self.product.title}: {self.rating}"

    class Meta:
        ordering = ['-id']
        unique_together = ('user', 'product')

