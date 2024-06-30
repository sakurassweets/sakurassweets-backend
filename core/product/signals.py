from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product)
def ensure_published_product_has_main_image(sender, instance, **kwargs):
    if instance.is_published:
        product_images = instance.image_set.all()
        has_images = product_images.exists()
        has_main_image = product_images.filter(main_image=True).exists()

        if not has_images:
            instance.is_published = False
            instance.save(update_fields=['is_published'])
        elif has_images and not has_main_image:
            next_image = product_images.first()
            next_image.main_image = True
            next_image.save()
