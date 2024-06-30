import os

from rest_framework import serializers

from image.models import Image


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.HyperlinkedIdentityField(view_name='image-detail')

    class Meta:
        model = Image
        fields = '__all__'
        extra_kwargs = {'image': {'required': False}}

    def update(self, instance, validated_data):
        # Check if the image field is in the validated_data
        if 'image' not in validated_data:
            # Only update the main_image field if the image field is not in the data
            instance.main_image = validated_data.get('main_image', instance.main_image)
            instance.save()
            return instance
        else:
            # Delete the old image file if it exists
            if instance.image:
                if os.path.isfile(instance.image.path):
                    os.remove(instance.image.path)
            return super().update(instance, validated_data)
