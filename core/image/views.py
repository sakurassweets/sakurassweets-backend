from rest_framework import permissions, exceptions, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.request import Request

from image.serializers import ImageSerializer
from image.models import Image
from components.image.validators import UpdateImageValidator
from components.general.caching.viewsets import CacheModelViewSet


class ImageViewSet(CacheModelViewSet):
    queryset = Image.objects.all()
    cache_key = "image"
    timeout = 60 * 5
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAdminUser()]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        else:
            return self.permission_classes

    def create(self, request: Request, *args, **kwargs):
        validator = UpdateImageValidator(request)
        related_to_id = request.data.get('related_to')
        if related_to_id:
            # Count existing images related to the review
            related_images_count = Image.objects.filter(related_to=related_to_id).count()
            if related_images_count >= 5:
                raise exceptions.ValidationError({"detail": "You cannot upload more than 5 images for this review."},
                                                 code=status.HTTP_400_BAD_REQUEST)
        if isinstance(result := validator.validate(), (str, dict)):
            raise exceptions.ValidationError({"detail": result}, code=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs):
        validator = UpdateImageValidator(request)
        if isinstance(result := validator.validate(), (str, dict)):
            raise exceptions.ValidationError({"detail": result}, code=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    @staticmethod
    def _validate_main_image(request: Request) -> str | None:
        """Validates main image adding.

        Validates that `main_image` in requests set to `True` and that
        product doesn't have main image yet

        Args:
            request: DRF's `Request` object.
        Returns:
            String with error if something wrong, else `None`.
        """
        related_to_id = request.data.get('related_to')
        if request.data.get('main_image') is None:
            return None

        has_main_image = Image.objects.filter(related_to=related_to_id, main_image=True)  # NOQA

        if has_main_image:
            return "This product already have main image"
