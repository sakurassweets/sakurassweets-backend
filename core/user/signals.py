from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from components.general.caching.delete_cache_keys import delete_keys_with_prefix
from user.models import User


@receiver(pre_save, sender=User)
def set_user_new_password_after_update(sender, instance: User, **kwargs) -> None:
    """Sets new password for user after updating.

    Args:
        sender: signal sender, a instance of Django's model.
        instance: exact instance that sends signal, `User` instance.
        **kwargs: keyword arguments enforced by @reciever to provide
            signal functionallity.
    """
    if not instance._state.adding:
        old_user = User.objects.get(pk=instance.pk)
        if instance.password != old_user.password:
            instance.set_password(instance.password)


names_map = {
    "producttype": "product_type",
    "pricecurrency": "price_currency",
    "cartitem": "cart_item"
}


def _get_cache_prefix(sender):
    sender_name = sender._meta.model_name
    prefix = names_map.get(sender_name, None) or sender_name
    return prefix


@receiver([post_save, post_delete])
def clear_cache(sender, instance, **kwargs) -> None:
    prefix = _get_cache_prefix(sender)
    try:
        pk = instance.id if instance.id else ''
        delete_keys_with_prefix(prefix, pk=pk)
    except AttributeError:
        pass
