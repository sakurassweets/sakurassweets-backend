from rest_framework import serializers

from product.models import Product, PriceCurrency, ProductType
from image.serializers import ImageSerializer
from image.models import Image


class ProductTypeSerializer(serializers.ModelSerializer):
    product_type_url = serializers.HyperlinkedIdentityField(view_name='product-type-detail')  # NOQA

    class Meta:
        model = ProductType
        fields = '__all__'


class PriceCurrencySerializer(serializers.ModelSerializer):
    price_currency_url = serializers.HyperlinkedIdentityField(view_name='price-currency-detail')  # NOQA

    class Meta:
        model = PriceCurrency
        fields = '__all__'


class _CustomImageSerializer(ImageSerializer):

    class Meta(ImageSerializer.Meta):
        model = Image
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer provides all actions related to Product model
    """
    product_url = serializers.HyperlinkedIdentityField(view_name='product-detail')  # NOQA
    product_type = ProductTypeSerializer()
    price_currency = PriceCurrencySerializer()
    images = _CustomImageSerializer(many=True, read_only=True, source='image_set')  # NOQA

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        __currency = instance.price_currency
        __product_type = instance.product_type
        representation['discount'] = f'{instance.discount} %'
        representation['product_type'] = 'UNDEFINED' if __product_type is None else __product_type.title
        representation['price_currency'] = 'UNDEFINED' if __currency is None else __currency.currency
        representation['price_currency_symbol'] = 'UNDEFINED' if __currency is None else __currency.currency_symbol
        return representation
