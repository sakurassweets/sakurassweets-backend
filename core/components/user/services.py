import re

from django.utils.translation import gettext as _

from rest_framework.validators import ValidationError

from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    UserAttributeSimilarityValidator
)
from django.core.exceptions import ValidationError as DjangoValidationError

from components.user.utils import clean_error_message

from components.user.constants import (
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH
)


class PasswordValidatorService:
    none_pass_error = _("Password should be not None.")
    common_pass_error = _("Password is too common.")
    _constants = {"min_len": MIN_PASSWORD_LENGTH,
                  "max_len": MAX_PASSWORD_LENGTH}
    _errors = []

    def __init__(self, password: str, user=None) -> None:
        self.password = password
        self.user = user

    def validate(self) -> None:

        self._validate_password()
        if len(self._errors) > 0:
            _errors = list(self._errors)
            self._errors.clear()
            raise ValidationError({"errors": _errors})

    def _validate_password(self) -> None:
        self._validate_password_length(
            self.password,
            self._constants['min_len'],
            self._constants['max_len']
        )
        self._validate_password_not_common(self.password)
        self._validate_password_user_similarity(self.password, self.user)
        self._validate_password_case(self.password)

    def _validate_password_length(self, password: str, min_len: int, max_len: int) -> None:
        validator = ValidatePasswordLengthService(min_len, max_len)
        self._validate_or_error(password, validator)

    def _validate_password_not_common(self, password: str) -> None:
        validator = CommonPasswordValidator()
        self._validate_or_error(password, validator)

    def _validate_password_user_similarity(self, password: str, user) -> None:
        validator = UserAttributeSimilarityValidator(max_similarity=0.55)
        self._validate_or_error(password, validator, user)

    def _validate_password_case(self, password: str) -> None:
        validator = ValidatePasswordCase()
        self._validate_or_error(password, validator)

    def _validate_or_error(self, password: str, validator, *args, **kwargs) -> None:
        try:
            validator.validate(password, *args, **kwargs)
        except DjangoValidationError as error:
            if not isinstance(validator, CommonPasswordValidator):
                error = str(error)
                self._errors.append(str(error)[2:-2])
            else:
                self._errors.append(self.common_pass_error)


class ValidatePasswordLengthService:
    min_pass_error = _(
        """
        Password must be at least %(value)s characters long.
        Got %(len)s instead.
        """
    )
    max_pass_error = _(
        """
        Password must be shorter than %(value)s characters long.
         Got %(len)s instead.
        """
    )

    def __init__(self, min_len: int, max_len: int) -> None:
        self.min_len = min_len
        self.max_len = max_len

    def validate(self, password) -> None:
        password_len = len(password)

        if password_len < self.min_len:
            message = self._generate_error(
                self.min_pass_error, self.min_len, password_len)

            raise DjangoValidationError(message)

        if password_len > self.max_len:
            message = self._generate_error(
                self.max_pass_error, self.max_len, password_len)

            raise DjangoValidationError(message)

    def get_help_text(self) -> str:
        return _(
            """
            Your password should have minimum %(min_len)d characters and maximum %(max_len)d characters
            """
        ) % {'min_len': self.min_len, 'max_len': self.max_len}

    @classmethod
    def _generate_error(cls, error: str, value: int, len_: int) -> str:
        error = error % {"value": value, "len": len_}
        cleaned_error = clean_error_message(error)
        return cleaned_error


class ValidatePasswordCase:
    def __init__(self, min_upper: int = 1, min_lower: int = 1) -> None:
        self.min_upper = min_upper
        self.min_lower = min_lower

    def validate(self, password: str) -> None:
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
            error_message = _(
                """
                Password must contain at least %(min_upper)d uppercase letter and %(min_lower)d lowercase letter.
                """
            )
            cleaned_error_message = clean_error_message(error_message)
            raise DjangoValidationError(cleaned_error_message % {"min_upper": self.min_upper,
                                                                 "min_lower": self.min_lower})

    def get_help_text(self) -> None:
        return _(
            "Your password must contain at least %(min_upper)d uppercase letter and %(min_lower)d lowercase letter."
        ) % {'min_upper': self.min_upper, 'min_lower': self.min_lower}
