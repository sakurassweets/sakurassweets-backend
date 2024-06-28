from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Image


@receiver(post_save, sender=Image)
def ensure_single_main_image(sender, instance, created, **kwargs):
    image_pk = instance.pk
    product = instance.related_to
    main_image = sender.objects.filter(related_to=product, main_image=True).exclude(pk=image_pk)
    if instance.main_image:
        # If it's not the first image but marked as main_image, unset main_image for other images
        main_image.update(main_image=False)
    elif not main_image.exists():
        instance.main_image = True
        instance.save()


@receiver(post_delete, sender=Image)
def set_product_unpublished_on_image_delete(sender, instance, **kwargs):
    product = instance.related_to
    product_images = sender.objects.filter(related_to=product)
    has_images = product_images.exists()
    if product.is_published and not has_images:
        product.is_published = False
        product.save()

    if instance.image:
        instance.image.delete(save=False)

    # Set another image as main_image if it exists
    if instance.main_image and has_images:
        next_image = product_images.first()
        if next_image:
            next_image.main_image = True
            next_image.save()
