import re
from abc import ABC, abstractmethod

from django.utils.translation import gettext as _

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


class BasePasswordValidator(ABC):
    @abstractmethod
    def validate(self, password: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def get_help_text(self) -> None:
        pass


class PasswordValidatorService:
    none_pass_error: str = _("Password should be not None.")
    common_pass_error: str = _("Password is too common.")
    _constants: dict = {"min_len": MIN_PASSWORD_LENGTH,
                        "max_len": MAX_PASSWORD_LENGTH}
    _errors: list = []

    def __init__(self, password: str, user=None) -> None:
        self.password = str(password)
        self.user = user

    def validate(self) -> list | None:

        self._validate_password()
        if len(self._errors) > 0:
            return self._return_errors()

    def _return_errors(self):
        _errors = list(self._errors)
        self._errors.clear()
        return _errors

    def _validate_password(self) -> None:
        """
        Method contains all validation calls and trigger them one by one
        """
        self._validate_password_length(
            self.password,
            self._constants['min_len'],
            self._constants['max_len']
        )
        self._validate_password_spacebars(self.password)
        self._validate_password_have_digit(self.password)
        self._validate_password_not_common(self.password)
        self._validate_password_user_similarity(self.password, self.user)
        self._validate_password_case(self.password)

    def _validate_password_have_digit(self, password: str) -> None:
        validator = ValidatePasswordHaveDigit()
        self._validate_or_error(password, validator)

    def _validate_password_spacebars(self, password: str) -> None:
        validator = ValidatePasswordSpecialCharacters()
        self._validate_or_error(password, validator)

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
        """
        Validate password with given validator and args
        If error occurs they added to class errors list
        """
        try:
            validator.validate(password, *args, **kwargs)
        except DjangoValidationError as error:
            if not isinstance(validator, CommonPasswordValidator):
                error = str(error)
                self._errors.append(str(error)[2:-2])
            else:
                self._errors.append(self.common_pass_error)


class ValidatePasswordLengthService(BasePasswordValidator):
    min_pass_error: str = _(
        """
        Password must be at least %(value)s characters long.
        Got %(len)s instead.
        """
    )
    max_pass_error: str = _(
        """
        Password must be shorter than %(value)s characters long.
        Got %(len)s instead.
        """
    )
    help_text: str = _(
        """
        Your password should have minimum %(min_len)d characters and maximum %(max_len)d characters
        """
    )

    def __init__(self, min_len: int, max_len: int) -> None:
        self.min_len = int(min_len)
        self.max_len = int(max_len)

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
        return self.help_text % {'min_len': self.min_len, 'max_len': self.max_len}

    @classmethod
    def _generate_error(cls, error: str, value: int, len_: int) -> str:
        error = error % {"value": value, "len": len_}
        cleaned_error = clean_error_message(error)
        return cleaned_error


class ValidatePasswordCase(BasePasswordValidator):
    """
    min_upper - Minimal value of uppercase letters in

    min_lower - Minimal value of lowercase letters in password
    """
    error_message: str = _(
        """
        Password must contain at least %(min_upper)d uppercase letter and %(min_lower)d lowercase letter.
        """
    )
    help_text: str = _(
        "Your password must contain at least %(min_upper)d uppercase letter and %(min_lower)d lowercase letter.")

    def __init__(self, min_upper: int = 1, min_lower: int = 1) -> None:
        self.min_upper = int(min_upper)
        self.min_lower = int(min_lower)

    def validate(self, password: str) -> None:
        """
        Validate if password has not enough lower/upper case letters
        """
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
            cleaned_error_message = clean_error_message(self.error_message)
            raise DjangoValidationError(cleaned_error_message % {"min_upper": (self.min_upper),
                                                                 "min_lower": self.min_lower})

    def get_help_text(self) -> None:
        return self.help_text % {'min_upper': (self.min_upper), 'min_lower': self.min_lower}


class ValidatePasswordSpecialCharacters(BasePasswordValidator):

    error_message: str = _(
        "Password should not contain any spacebars.")
    help_text: str = _(
        "Your password should not contain any spacebars.")

    def validate(self, password: str) -> None:
        if len(password.split(' ')) > 1:
            raise DjangoValidationError(self.error_message)

    def get_help_text(self):
        return self.help_text


class ValidatePasswordHaveDigit(BasePasswordValidator):

    error_message: str = _("Password should contain at least one digit.")
    help_text: str = _("You`r password should contain at least one digit.")
    digits_amount: int = 1

    def __init__(self, digits_amount: int = None) -> None:
        if digits_amount is not None:
            try:
                self.digits_amount = int(digits_amount)
            except TypeError:
                raise TypeError(
                    f"digits_amount should be a int, but got {type(digits_amount).__name__}")
            except ValueError:
                raise TypeError(
                    f"digits_amount should be a int, but got {type(digits_amount).__name__}")

    def validate(self, password: str, *args, **kwargs) -> None:
        if not any(c.isdigit() for c in password):
            raise DjangoValidationError(self.error_message)

    def get_help_text(self) -> None:
        return self.help_text
