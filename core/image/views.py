from rest_framework import viewsets, permissions, exceptions

from image.serializers import ImageSerializer
from image.models import Image


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAdminUser()]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        else:
            return self.permission_classes

    def create(self, request, *args, **kwargs):
        related_to_id = request.data.get('related_to')
        if Image.objects.filter(related_to=related_to_id, main_image=True).exists():
            raise exceptions.APIException(
                "This product already have main image")

        return super().create(request, *args, **kwargs)
