from rest_framework import viewsets, permissions

from image.serializers import ImageSerializer
from image.models import Image


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.AllowAny,]
