from rest_framework import serializers

from product.models import Product, PriceCurrency, ProductType
from image.serializers import ImageSerializer
from image.models import Image


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = '__all__'


class PriceCurrencySerializer(serializers.ModelSerializer):

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
        representation['discount'] = f'{instance.discount} %'
        representation['product_type'] = instance.product_type.title
        representation['price_currency'] = instance.price_currency.currency
        representation['price_currency_symbol'] = instance.price_currency.currency_symbol  # NOQA
        return representation
