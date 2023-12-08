from django.db import models


class ProductType(models.Model):
    title = models.CharField('Тип продукту', max_length=255)

    def __str__(self):
        return f'ID: {self.id} | Type: {self.title}'


class PriceCurrency(models.Model):
    currency_symbol = models.CharField('Валютний символ',
                                       unique=True,
                                       max_length=10,
                                       blank=False,
                                       null=False,
                                       default='₴')
    currency = models.CharField('Валюта', unique=True, max_length=255, blank=False, null=False)  # NOQA
    country = models.CharField('Країна', max_length=255, blank=False, null=False)  # NOQA

    def __str__(self):
        return f'{self.currency}'


class Product(models.Model):
    title = models.CharField('Назва', max_length=255, blank=False, null=False)
    price = models.DecimalField('Ціна',
                                max_digits=8,
                                decimal_places=2,
                                blank=False,
                                null=False)
    price_currency = models.ForeignKey(PriceCurrency,
                                       verbose_name='Валюта',
                                       on_delete=models.DO_NOTHING,
                                       blank=False,
                                       null=False,)
    product_type = models.ForeignKey(ProductType,
                                     verbose_name='Тип продукту',
                                     on_delete=models.DO_NOTHING,
                                     blank=False,
                                     null=False)
    description = models.TextField('Опис', max_length=6000, blank=True, null=False)  # NOQA
    quantity_in_stock = models.PositiveIntegerField('Кількість на складі', blank=False, null=False)  # NOQA
    product_quantity = models.CharField('Обсяг продукту', max_length=255, blank=False, null=False)  # NOQA
    discount = models.PositiveSmallIntegerField('Знижка', default=0, blank=True, null=True)  # NOQA
    rating = models.FloatField('Рейтинг', blank=True, null=True)
    components = models.TextField('Склад', blank=True, null=True)

    # def calculate_discount(self):
    #     pass

    def __str__(self):
        return f'ID: {self.id} | Title: "{self.title}"'

    class Meta:
        ordering = ['-id']
