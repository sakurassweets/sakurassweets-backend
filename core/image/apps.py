from django.apps import AppConfig


class ImageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'image'

    def ready(self) -> None:
        import image.signals # NOQA
