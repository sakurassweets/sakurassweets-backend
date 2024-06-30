from rest_framework import serializers
from .models import ProductReview


class ReviewListSerializer(serializers.ModelSerializer):
    review_url = serializers.HyperlinkedIdentityField(view_name='review-detail')  # NOQA
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'product', 'rating', 'text', 'review_url']

    def to_representation(self, instance):
        # Customize the serialization process
        representation = super().to_representation(instance)
        # Add a user field to the representation
        representation['user'] = str(instance.user)
        return representation
