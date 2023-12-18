from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from rest_framework.exceptions import ValidationError

from components.user.services.password_validation import PasswordValidatorService
from components.general.caching.delete_cache_keys import delete_keys_with_prefix
from components.user.services.email_validation import EmailValidatorService

from user.models import User


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
    delete_keys_with_prefix('user', pk=pk)


@receiver(post_delete, sender=User)
def clear_cache_post_delete(sender, instance: User, **kwargs) -> None:
    pk = instance.id if instance.id else ''
    delete_keys_with_prefix('user', pk=pk)
