import re
from abc import ABC, abstractmethod
from copy import copy

from django.utils.translation import gettext as _

from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    UserAttributeSimilarityValidator
)
from django.core.exceptions import ValidationError as DjangoValidationError

from components.user import constants, utils


class BasePasswordValidator(ABC):
    @abstractmethod
    def validate(self, password: str, *args, **kwargs) -> None:
        pass


class PasswordValidator(BasePasswordValidator):
    @abstractmethod
    def get_help_text(self) -> str:
        pass


class PasswordValidatorService(BasePasswordValidator):
    none_pass_error: str = _("Password should be not None.")
    _errors: list = []
    constants = constants.PASSWORD_CONSTANTS

    def __init__(self, password: str, user=None) -> None:
        self.password = str(password)
        self.user = user
        self.set_validators()

    def validate(self) -> list | None:
        self._validate_password()
        if len(self._errors) > 0:
            return self._return_errors()

    def _return_errors(self) -> list:
        _errors = copy(self._errors)
        self._errors.clear()
        return _errors

    def _validate_password(self) -> None:
        """
        Method contains all validation calls and trigger them one by one
        """
        for validator in self._validators:
            self._validate_or_error(self.password, validator)

    def _validate_or_error(self, password: str, validator, *args, **kwargs) -> None:
        """
        Validate password with given validator and args
        If error occurs they added to class errors list
        """
        try:
            validator.validate(password, *args, **kwargs)
        except DjangoValidationError as error:
            error = str(error)
            self._errors.append(str(error)[2:-2])

    def set_validators(self, validators: list[object] = None) -> None:
        """
        Input:
        - validators - a list of validator instances.

        example of list: [CommonValidator(), CaseValidator(), ...]

        validator should have `validate()` method and get as arguments only
        password. Other arguments should be defined through validator constructor.
        """
        default_validators = self.__default_validators

        if validators is not None:
            if isinstance(validators, list):
                self._validators = validators
            else:
                raise TypeError(
                    f"validators should be a list, got '{type(validators).__name__}' instead")
        else:
            self._validators = default_validators

    def add_validator(self, validator: BasePasswordValidator | PasswordValidator | object) -> None:
        """
        Input:
        - validator - a validator instance.

        should be inputed like: CommonValidator()

        validato should have `validate()` method and get as arguments only
        password. Other arguments should be defined through validator constructor.
        """
        self._validators.append(validator)

    @property
    def __default_validators(self) -> list:
        default_validators = [
            PasswordLengthValidator(
                self.constants['min_len'],
                self.constants['max_len']
            ),
            PasswordSpacebarsValidator(),
            PasswordLatinValidator(),
            PasswordHaveDigitValidator(
                min_digits=self.constants['min_digits']
            ),
            PasswordCommonValidator(),
            PasswordUserAttributeSimilarityValidator(
                user=self.user,
                max_similarity=self.constants['max_similarity']
            ),
            PasswordCaseValidator(),
        ]
        return default_validators


class PasswordLatinValidator(PasswordValidator):

    _error_message = _("Only latin characters allowed in password")
    _help_text = _("Password must contain only latin characters")

    def validate(self, password: str) -> None:
        regex_cyrillic = r'[А-Яа-яІЇЁёЄєҐґ]'

        if re.search(regex_cyrillic, password):
            raise DjangoValidationError(self._error_message)

    def get_help_text(self) -> None:
        return self._help_text


class PasswordCommonValidator(PasswordValidator, CommonPasswordValidator):
    """
    This class gets all the `common password validation` from CommonPasswordValidator but also
    inheirts from `PasswordValidator` which is interface for validators
    """

    def __init__(self, *args, **kwargs):
        CommonPasswordValidator().__init__(*args, **kwargs)

    def validate(self, password):
        return CommonPasswordValidator().validate(password)

    def get_help_text(self) -> None:
        return CommonPasswordValidator().get_help_text()


class PasswordUserAttributeSimilarityValidator(PasswordValidator, UserAttributeSimilarityValidator):
    """
    This class gets all the `user attribute similarity validation` from CommonPasswordValidator
    but also inheirts from `PasswordValidator` which is interface for validators
    """

    def __init__(self, user, *args, **kwargs):
        self.user = user
        UserAttributeSimilarityValidator().__init__(*args, **kwargs)

    def validate(self, password: str) -> None:
        return UserAttributeSimilarityValidator().validate(password, self.user)

    def get_help_text(self) -> None:
        return UserAttributeSimilarityValidator().get_help_text()


class PasswordLengthValidator(PasswordValidator):
    _min_pass_error: str = _("Password must be at least %(value)s characters long.Got %(len)s instead.")  # NOQA
    _max_pass_error: str = _("Password must be shorter than %(value)s characters long.Got %(len)s instead.")  # NOQA
    _help_text: str = _("Your password should have minimum %(min_len)d characters and maximum %(max_len)d characters")  # NOQA

    def __init__(self, min_len: int, max_len: int) -> None:
        self.min_len = int(min_len)
        self.max_len = int(max_len)

    def validate(self, password: str) -> None:
        password_len = len(password)

        if password_len < self.min_len:
            message = self._generate_error(
                self._min_pass_error, self.min_len, password_len)

            raise DjangoValidationError(message)

        if password_len > self.max_len:
            message = self._generate_error(
                self._max_pass_error, self.max_len, password_len)

            raise DjangoValidationError(message)

    def get_help_text(self) -> str:
        return self._help_text % {'min_len': self.min_len, 'max_len': self.max_len}

    @classmethod
    def _generate_error(cls, error: str, value: int, len_: int) -> str:
        error = error % {"value": value, "len": len_}
        cleaned_error = utils.clean_error_message(error)
        return cleaned_error


class PasswordCaseValidator(PasswordValidator):
    """
    min_upper - Minimal value of uppercase letters in

    min_lower - Minimal value of lowercase letters in password
    """
    _error_message: str = _("Password must contain at least %(min_upper)d uppercase letter and %(min_lower)d lowercase letter.")  # NOQA
    _help_text: str = _("Your password must contain at least %(min_upper)d uppercase letter and %(min_lower)d lowercase letter.")  # NOQA

    def __init__(self, min_upper: int = 1, min_lower: int = 1) -> None:
        self.min_upper = int(min_upper)
        self.min_lower = int(min_lower)

    def validate(self, password: str) -> None:
        """
        Validate if password has not enough lower/upper case letters
        """
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
            error_message = utils.clean_error_message(self._error_message)
            raise DjangoValidationError(error_message % {"min_upper": (self.min_upper),
                                                         "min_lower": self.min_lower})

    def get_help_text(self) -> None:
        return self._help_text % {'min_upper': (self.min_upper), 'min_lower': self.min_lower}


class PasswordSpacebarsValidator(PasswordValidator):

    _error_message: str = _("Password should not contain any spacebars.")
    _help_text: str = _("Your password should not contain any spacebars.")

    def validate(self, password: str) -> None:
        if password.find(' ') != -1:
            raise DjangoValidationError(self._error_message)

    def get_help_text(self):
        return self._help_text


class PasswordHaveDigitValidator(PasswordValidator):
    _error_message: str = _("Password should contain at least %(value)d digit.")  # NOQA
    _help_text: str = _("You`r password should contain at least %(value)d digit.")  # NOQA

    def __init__(self, min_digits: int = 0) -> None:
        if isinstance(min_digits, int):
            self.min_digits = min_digits
        else:
            raise TypeError(
                f"min_digits should be 'int', got '{type(min_digits).__name__}' instead")

    def validate(self, password: str) -> None:
        digits = self._get_digits(password)
        if len(digits) < self.min_digits:
            raise DjangoValidationError(self._error_message % {
                "value": self.min_digits
            })

    def get_help_text(self) -> None:
        return self._help_text

    @staticmethod
    def _get_digits(password: str) -> list:
        _digits = [c for c in password if c.isdigit()]
        return _digits
