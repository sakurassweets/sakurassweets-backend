from django.db import models
from product.models import Product


def image_dir_path(instance: 'Image', filename: str) -> str:

    # file will be uploaded to MEDIA_ROOT / product_<id>/<filename>
    return f'product_{instance.related_to.id}/{filename}'


class Image(models.Model):
    # Main image can be only one for product and will be shown as first image
    image = models.ImageField('Зображення', blank=False, null=False, upload_to=image_dir_path)  # NOQA
    main_image = models.BooleanField('Основне фото', default=False)
    # Product that image related to
    related_to = models.ForeignKey(Product,
                                   verbose_name='Відноситься до',
                                   on_delete=models.DO_NOTHING,
                                   null=False,
                                   blank=False)

    def __str__(self):
        return f'{self.id} | {self.image.name}'
