from rest_framework import serializers
from .models import ProductRating


class RatingListSerializer(serializers.ModelSerializer):
    rating_url = serializers.HyperlinkedIdentityField(view_name='rating-detail')  # NOQA

    class Meta:
        model = ProductRating
        fields = '__all__'
