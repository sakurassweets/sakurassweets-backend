from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

from user.validators import PasswordValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str = None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        PasswordValidator.validate_password_length(password)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email адреса", unique=True)
    password = models.CharField("Пароль", max_length=128)

    created_at = models.DateTimeField("Створено", auto_now=True)
    updated_at = models.DateTimeField("Оновлено", auto_now_add=True)

    is_superuser = models.BooleanField("Супер користувач", default=False)
    is_staff = models.BooleanField("Персонал", default=False)
    is_active = models.BooleanField("Активний", default=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_permissions')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
