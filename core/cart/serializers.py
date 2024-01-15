from rest_framework import serializers

from cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_url = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True, source='product')  # NOQA
    cart_item_url = serializers.HyperlinkedIdentityField(view_name='cart-item-detail')  # NOQA

    class Meta:
        model = CartItem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = f'{instance.product.title}'
        return representation


class _CustomCartItemSerializer(CartItemSerializer):

    class Meta:
        model = CartItem
        fields = ['product', 'product_url', 'cart_item_url']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = f'{instance.product.title}'  # NOQA
        return representation


class CartSerializer(serializers.ModelSerializer):

    items = _CustomCartItemSerializer(many=True, read_only=True, source='cartitem_set')  # NOQA
    cart_url = serializers.HyperlinkedIdentityField(view_name='cart-detail')

    class Meta:
        model = Cart
        fields = '__all__'
