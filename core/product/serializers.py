from rest_framework import serializers

from product.models import Product, PriceCurrency, ProductType


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = ['title']


class PriceCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = PriceCurrency
        fields = ['currency']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer provides all actions related to Product model
    """
    product_url = serializers.HyperlinkedIdentityField(view_name='product-detail')  # NOQA
    product_type = ProductTypeSerializer()
    price_currency = PriceCurrencySerializer()

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Use the author's name instead of id
        representation['discount'] = f'{instance.discount} %'
        representation['product_type'] = instance.product_type.title
        representation['price_currency'] = instance.price_currency.currency
        return representation
