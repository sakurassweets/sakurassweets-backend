import copy

from django.utils.translation import gettext as _
from django.contrib.auth.base_user import AbstractBaseUser

from rest_framework.exceptions import ValidationError

from components.user.services.email_validation import EmailValidatorService
from components.user.services.password_validation import PasswordValidatorService

from user.models import User


class UserValidator:

    _errors = {}

    @classmethod
    def validate(cls, password: str, user: User) -> None:
        """Validates user password and email.

        Validates password and email using two different validators:
        `PasswordValidator` and `EmailValidator`.
        Collects errors from both validations and raises all together.

        Args:
            password: String object of password that being validated.
            user: Object of user, `User` instance.

        """
        pass_errors = cls._validate_password(password, user)
        email_errors = cls._validate_email(user)
        cls._raise_errors(cls, pass_errors, email_errors)

    def _raise_errors(self, pass_errors: list, email_errors: list) -> None:

        if email_errors:
            self._errors["email_errors"] = email_errors

        if pass_errors:
            self._errors["password_errors"] = pass_errors

        if self._errors:
            _errors = copy.deepcopy(self._errors)
            self._errors.clear()
            raise ValidationError({"detail": _errors})

    @staticmethod
    def _validate_password(password: str, user: User) -> list | None:
        password_validator = PasswordValidator()
        pass_errors = password_validator.validate(password, user)
        return pass_errors

    @staticmethod
    def _validate_email(user: User) -> list | None:
        email_validator = EmailValidator()
        email_errors = email_validator.validate(user)
        return email_errors


class EmailValidator:
    none_email_error: str = _("Email should be not None.")

    @classmethod
    def validate(cls, user: User) -> list | None:
        if isinstance(user, User):
            email = user.email
        else:
            email = user

        if email is not None:
            validator = EmailValidatorService(email)
            return validator.validate()
        else:
            return cls.none_email_error


class PasswordValidator:
    none_pass_error: str = _("Password should be not None.")

    @classmethod
    def validate(cls, password: str, user: User) -> list | None:
        if isinstance(user, str):
            user = _MockUser(user)

        if password is not None:
            validator = PasswordValidatorService(password, user)
            return validator.validate()
        else:
            return cls.none_pass_error


class _MockUser(AbstractBaseUser):
    """Creates mock User object.

    Used to complete user attribute similarity validaton since it used:
    >>> getattr(user, attribute_name, None)
    """

    def __init__(self, email: str) -> None:
        self.email = email

    class Meta:
        abstract = True
