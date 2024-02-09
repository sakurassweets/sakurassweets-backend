import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            "price": ["gte", "lte"],
            "rating": ["gte", "lte"],
            "quantity_in_stock": ["gte", "lte"]
        }
