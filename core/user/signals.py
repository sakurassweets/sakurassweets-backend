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


@receiver(post_save, sender=User)
def clear_cache_post_save(sender, instance: User, **kwargs) -> None:
    pk = instance.id if instance.id else ''
    delete_keys_with_prefix('user', pk=pk)


@receiver(post_delete, sender=User)
def clear_cache_post_delete(sender, instance: User, **kwargs) -> None:
    pk = instance.id if instance.id else ''
    delete_keys_with_prefix('user', pk=pk)
