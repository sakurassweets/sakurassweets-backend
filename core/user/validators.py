from django.core.exceptions import ValidationError


class PasswordValidator:
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 40

    @classmethod
    def validate_password_length(cls, password: str) -> None:
        if len(password) < cls.MIN_PASSWORD_LENGTH:
            raise ValidationError(
                f"Password must be at least {cls.MIN_PASSWORD_LENGTH} characters long.")
        if len(password) > cls.MAX_PASSWORD_LENGTH:
            raise ValidationError(
                f"Password must be shorter than {cls.MAX_PASSWORD_LENGTH} characters long.")
