from django.db.models.signals import pre_save
from django.dispatch import receiver

from rest_framework.exceptions import ValidationError

from components.user.services.password_validation import PasswordValidatorService
from components.user.services.email_validation import EmailValidatorService
from user.models import User


@receiver(pre_save, sender=User)
def validate_user_fields_after_update(sender, instance: User, **kwargs):
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
