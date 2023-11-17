from rest_framework.validators import ValidationError

from components.user.services import PasswordValidatorService


class PasswordValidator:
    # TODO: Logg validation
    none_pass_error = (
        """
        Password should be not None.
        """
    )

    @classmethod
    def validate(cls, password: str, user) -> None:
        if password is not None:
            validator = PasswordValidatorService(password, user)
            validator.validate()
        else:
            raise ValidationError(cls.none_pass_error)
