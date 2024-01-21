from django.db import models
from product.models import Product


def image_dir_path(instance: 'Image', filename: str) -> str:

    # return MEDIA_ROOT/product_<id>/<filename>
    return f'product_{instance.related_to.id}/{filename}'


class Image(models.Model):
    # Main image can be only one for product and will be shown as first image
    image = models.ImageField('Зображення', blank=False, null=False, upload_to=image_dir_path)  # NOQA
    main_image = models.BooleanField('Основне фото', default=False)
    related_to = models.ForeignKey(Product,
                                   verbose_name='Відноситься до',
                                   on_delete=models.DO_NOTHING,
                                   null=False,
                                   blank=False)

    def __str__(self):
        return f'ID: {self.id} | Related to: {self.related_to.title} | Filename: {self.image.name}'

    class Meta:
        ordering = ['-id']
