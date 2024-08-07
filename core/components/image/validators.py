from rest_framework.request import Request
# from image.models import Image


class UpdateImageValidator:
    error_messages = {
        "required_fields": "This field is required.",
    }
    REQUIRED_FIELDS = ['image', 'related_to']

    def __init__(self, request: Request):
        self.request = request

    def validate(self):
        if self.request.method == "PUT":
            if isinstance(result := self._validate_required_fields(), dict):
                return result

        return True

    def _validate_required_fields(self) -> dict[str, str] | None:
        errors: dict = {}
        for field in self.REQUIRED_FIELDS:
            if field not in self.request.data:
                errors[field] = self.error_messages["required_fields"]

        return errors if errors else None
