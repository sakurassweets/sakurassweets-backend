from django.core.exceptions import ValidationError

from components.user.constants import (
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH
)


class PasswordValidator:
    # TODO: Logg validation result
    min_pass_error = "Password must be at least %(value)s characters long."
    max_pass_error = "Password must be shorter than %(value)s characters long."
    none_pass_error = "Expected password but got None instead"

    @classmethod
    def validate_password_length(cls, password: str) -> None:
        if password is None:
            raise ValidationError(cls.none_pass_error)

        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValidationError(cls.min_pass_error % MIN_PASSWORD_LENGTH)

        if len(password) > MAX_PASSWORD_LENGTH:
            raise ValidationError(cls.max_pass_error % MAX_PASSWORD_LENGTH)
