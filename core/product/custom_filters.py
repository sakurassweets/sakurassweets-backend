import django_filters

from rest_framework.exceptions import APIException

from .models import Product


class ProductFilter(django_filters.FilterSet):

    product_type = django_filters.CharFilter(
        method='filter_product_type'
    )

    def filter_product_type(self, queryset, name, value):
        values = value.split(',')

        for v in values:
            if not v.isdigit():
                raise APIException(f"Filter can contain only id's, not '{v}'")

        return queryset.filter(product_type__id__in=values)

    class Meta:
        model = Product
        fields = {
            "price": ["gte", "lte"],
            "rating": ["gte", "lte"],
            "quantity_in_stock": ["gte", "lte"]
        }
