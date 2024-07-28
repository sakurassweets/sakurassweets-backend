from collections import OrderedDict

from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_url = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True, source='product')  # NOQA
    cart_item_url = serializers.HyperlinkedIdentityField(view_name='cart-item-detail')  # NOQA
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.select_related('cart_owner'), many=False)

    class Meta:
        model = CartItem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = f'{instance.product.title}'
        return representation


class _CustomCartItemSerializer(CartItemSerializer):
    """Provides only `product`, `product_url` and `cart_item_url` fields."""

    class Meta:
        model = CartItem
        fields = ['product', 'product_url', 'cart_item_url']

    def to_representation(self, instance: CartItem) -> OrderedDict:
        """Sets final representation of fields.

        Method modifies some fields to properly display them,
        this makes output readability and usability better.

        Args:
            instance: an serializeable object instance, `CartItem`
                instance in this case.

        Returns:
            Ordered dictionary of representation.
        """
        representation = super().to_representation(instance)
        representation['product'] = f'{instance.product.title}'  # NOQA
        return representation


class CartSerializer(serializers.ModelSerializer):

    items = _CustomCartItemSerializer(many=True, read_only=True, source='cartitem_set')  # NOQA
    cart_url = serializers.HyperlinkedIdentityField(view_name='cart-detail')

    class Meta:
        model = Cart
        fields = '__all__'
