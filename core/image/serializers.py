from rest_framework import serializers

from image.models import Image


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.HyperlinkedIdentityField(view_name='image-detail')  # NOQA

    class Meta:
        model = Image
        fields = '__all__'
