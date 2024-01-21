from rest_framework import viewsets, permissions, exceptions, status

from image.serializers import ImageSerializer
from image.models import Image
from components.image.validators import UpdateImageValidator


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
        if isinstance(result := self._validate_main_image(request), str):
            raise exceptions.ValidationError({"detail": result},
                                             code=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def _validate_main_image(self, request):
        related_to_id = request.data.get('related_to')
        if request.data.get('main_image').lower() == "true":
            request_main_image = True
        else:
            request_main_image = False

        has_main_image = Image.objects.filter(
            related_to=related_to_id, main_image=True)

        if has_main_image and request_main_image:
            return "This product already have main image"

    def update(self, request, *args, **kwargs):
        validator = UpdateImageValidator(request)

        if isinstance(result := validator.validate(), (str, dict)):
            raise exceptions.ValidationError({"detail": result},
                                             code=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)
