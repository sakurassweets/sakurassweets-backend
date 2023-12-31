from django.utils.translation import gettext as _

from rest_framework.validators import ValidationError

from components.user.services.email_validation import EmailValidatorService
from components.user.services.password_validation import PasswordValidatorService


class UserValidator:

    _errors: list = {}

    @classmethod
    def validate(cls, password: str, user) -> None:
        """
        Validates user password and email
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
            _errors = dict(self._errors)
            self._errors.clear()
            raise ValidationError({"detail": _errors})

    @staticmethod
    def _validate_password(password: str, user) -> list | None:
        password_validator = PasswordValidator()
        pass_errors = password_validator.validate(password, user)
        return pass_errors

    @staticmethod
    def _validate_email(user) -> list | None:
        email_validator = EmailValidator()
        email_errors = email_validator.validate(str(user))
        return email_errors


class EmailValidator:
    none_email_error: str = _("Email should be not None.")

    @classmethod
    def validate(cls, email: str) -> list | None:
        if email is not None:
            validator = EmailValidatorService(email)
            return validator.validate()
        else:
            return cls.none_email_error


class PasswordValidator:
    none_pass_error: str = _("Password should be not None.")

    @classmethod
    def validate(cls, password: str, user) -> list | None:
        if password is not None:
            validator = PasswordValidatorService(password, user)
            return validator.validate()
        else:
            return cls.none_pass_error
