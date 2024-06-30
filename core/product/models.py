from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ProductType(models.Model):
    title = models.CharField('Тип продукту',
                             max_length=255,
                             blank=False,
                             null=False)

    def __str__(self):
        return f'ID: {self.id} | Type: {self.title}'


class PriceCurrency(models.Model):
    currency_symbol = models.CharField('Валютний символ',
                                       unique=True,
                                       max_length=10,
                                       blank=False,
                                       null=False)
    currency = models.CharField('Валюта', unique=True, max_length=255, blank=False, null=False)  # NOQA
    country = models.CharField('Країна', max_length=255, blank=False, null=False)  # NOQA

    def __str__(self):
        return f'{self.currency}'

    class Meta:
        ordering = ['-id']


class Product(models.Model):
    title = models.CharField('Назва', max_length=70, blank=False, null=False)
    price = models.DecimalField('Ціна',
                                max_digits=8,
                                decimal_places=2,
                                blank=False,
                                null=False)
    price_currency = models.ForeignKey(PriceCurrency,
                                       verbose_name='Валюта',
                                       on_delete=models.SET_NULL,
                                       blank=False,
                                       null=True)
    product_type = models.ForeignKey(ProductType,
                                     verbose_name='Тип продукту',
                                     on_delete=models.SET_NULL,
                                     blank=False,
                                     null=True,
                                     related_name='products')
    description = models.TextField('Опис', max_length=500, default='', blank=True, null=False)  # NOQA
    quantity_in_stock = models.PositiveIntegerField('Кількість на складі', blank=False, null=False)  # NOQA
    product_quantity = models.CharField('Обсяг продукту', max_length=255, blank=False, null=False)  # NOQA
    discount = models.PositiveSmallIntegerField('Знижка', default=0, blank=True, null=True)  # NOQA
    rating = models.FloatField(
        'Рейтинг',
        default=0.0,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ]
    )
    components = models.TextField('Склад', max_length=500, default='', blank=True, null=True)
    manufacturer = models.CharField('Виробник', max_length=100, blank=False, null=False)
    is_published = models.BooleanField('Опубліковано', default=False, null=False, blank=False)

    def __str__(self):
        _title = self.title

        if not _title.startswith('"'):
            _title = f'"{_title}'

        if not _title.endswith('"'):
            _title = f'{_title}"'

        return f'ID: {self.id} | Title: {_title}'

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method
        super().save(*args, **kwargs)
        # self.validate_related_objects()

    class Meta:
        ordering = ['-id']
