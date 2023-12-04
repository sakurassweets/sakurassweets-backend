from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from rest_framework.exceptions import ValidationError

from components.user.services.password_validation import PasswordValidatorService
from components.user.services.email_validation import EmailValidatorService

from user.models import User
from user.tasks import send_welcome_email


def _delete_keys_with_prefix(prefix: str, pk: str) -> None:
    all_keys = cache.keys('*')  # Get all keys in the cache
    # Filter keys that start with the specified prefix
    keys_to_delete = [key for key in all_keys if key.startswith(prefix)]
    # Delete the keys
    for key in keys_to_delete:
        if key.startswith('user_retrieve'):
            if key in [f'user_retrieve_{pk}', f'user_retrieve_{pk}_status_code']:
                cache.delete(key)
            else:
                continue
        cache.delete(key)


@receiver(pre_save, sender=User)
def validate_user_fields_after_update(sender, instance: User, **kwargs) -> None:
    if not instance._state.adding:
        old_user = User.objects.get(pk=instance.pk)
        if instance.password != old_user.password:
            validator = PasswordValidatorService(
                password=instance.password,
                user=instance
            )
            errors = validator.validate()
            if errors is not None:
                raise ValidationError({"detail": errors})
            instance.set_password(instance.password)

        if instance.email != old_user.email:
            validator = EmailValidatorService(instance.email)
            errors = validator.validate()
            if errors is not None:
                raise ValidationError({"detail": errors})


@receiver(post_save, sender=User)
def clear_cache_post_save(sender, instance: User, **kwargs) -> None:
    pk = instance.id if instance.id else ''
    _delete_keys_with_prefix('user_', pk=pk)


@receiver(post_delete, sender=User)
def clear_cache_post_delete(sender, instance: User, **kwargs) -> None:
    pk = instance.id if instance.id else ''
    _delete_keys_with_prefix('user_', pk=pk)


@receiver(post_save, sender=User)
def send_welcome_email_signal(sender, instance, **kwargs) -> None:
    data = {
        'user_email': instance.email
    }
    send_welcome_email.delay(data)
