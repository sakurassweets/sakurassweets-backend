from abc import ABC, abstractmethod
from typing import Literal
import copy
import re

from django.utils.translation import gettext as _

from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from django.core.exceptions import ValidationError as DjangoValidationError

from components.user import constants

from user.models import User


class BasePasswordValidator(ABC):
    @abstractmethod
    def validate(self, password: str, *args, **kwargs) -> None:
        pass


class PasswordValidator(BasePasswordValidator):
    @abstractmethod
    def get_help_text(self) -> str:
        pass


class PasswordValidatorService(BasePasswordValidator):
    _error_messages: dict = {
        "no_method": "'validators' list should contain only classes with 'validate()' method.",
        "validators_misstype": "validators should be a list, got '%(type)s' instead"
    }
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
        _errors = copy.deepcopy(self._errors)
        self._errors.clear()
        return _errors

    def _validate_password(self) -> None:
        for validator in self._validators:
            self._validate_or_error(self.password, validator)

    def _validate_or_error(self, password: str, validator, *args, **kwargs) -> None:
        """Validates password with given validator and args.

        If error occurs they added to class errors list

        Args:
            password: String of user password that being validated.
            validator: Validator object that validates password.
        """
        try:
            validator.validate(password, *args, **kwargs)
        except DjangoValidationError as error:
            error = str(error)
            self._errors.append(str(error)[2:-2])

    def set_validators(self, validators: list[object] = None) -> Literal[True]:
        """Sets custom list of validators if provided.

        Example of list: [CommonValidator(), CaseValidator(), ...]

        Validator should have `validate()` method and get as arguments only
        password. Other arguments should be defined through validator constructor.

        Args:
            validators: A `list` of validator instances.

        Returns:
            True if validators set.

        Raises:
            TypeError: if validator in list is don't have validate() method
                or `validators` isn't `list` instance..
        """

        if validators is None:
            validators = self.__default_validators

        if not isinstance(validators, list):
            raise TypeError(self._error_messages["validators_misstype"] % {
                "type": type(validators).__name__
            })

        if not self.__check_validators(validators):
            raise TypeError(self._error_messages["no_method"])

        self._validators = validators
        return True

    def add_validator(self, validator: object) -> None:
        """Adds validator to existing list of validators.

        Validator should have `validate()` method and get as arguments only
        password. Other arguments should be defined through validator constructor.

        Args:
            validator: A validator instance. should be inputed
                like: `CommonValidator()`
        """
        self._validators.append(validator)

    @staticmethod
    def __check_validators(validators: list) -> bool:
        for validator in validators:
            if not hasattr(validator, 'validate'):
                return False
        return True

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
        """Validates that password contain only latin characters.

        Args:
            password: String object of password that being validated.

        Raises:
            `DjangoValidationError` if found non-latin character.
        """
        regex_cyrillic = r'[А-Яа-яІЇЁёЄєҐґ]'

        if re.search(regex_cyrillic, password):
            raise DjangoValidationError(self._error_message)

    def get_help_text(self) -> None:
        return self._help_text


class PasswordUserAttributeSimilarityValidator(PasswordValidator, UserAttributeSimilarityValidator):
    """Provides validation for user attributes similarity.

    Gets all the user attribute similarity validation
    from CommonPasswordValidator.
    """

    def __init__(self, user: User, *args, **kwargs) -> None:
        self.user = user
        UserAttributeSimilarityValidator().__init__(*args, **kwargs)

    def validate(self, password: str) -> None:
        return UserAttributeSimilarityValidator().validate(password, self.user)

    def get_help_text(self) -> None:
        return UserAttributeSimilarityValidator().get_help_text()


class PasswordLengthValidator(PasswordValidator):

    _error_messages: dict = {
        "min_pass": _("Password must be at least %(value)s characters long. Got %(len)s instead."),
        "max_pass": _("Password must be shorter than %(value)s characters long. Got %(len)s instead.")
    }
    _help_text: str = _("Your password should have minimum %(min_len)d"
                        " characters and maximum %(max_len)d characters")

    def __init__(self, min_len: int, max_len: int) -> None:
        self.min_len = int(min_len)
        self.max_len = int(max_len)

    def validate(self, password: str) -> None:
        password_len = len(password)

        if password_len < self.min_len:
            message = self._error_messages["min_pass"] % {
                "value": self.min_len,
                "len": password_len
            }
            raise DjangoValidationError(message)

        if password_len > self.max_len:
            message = self._error_messages["max_pass"] % {
                "value": self.max_len,
                "len": password_len
            }
            raise DjangoValidationError(message)

    def get_help_text(self) -> str:
        return self._help_text % {'min_len': self.min_len,
                                  'max_len': self.max_len}


class PasswordCaseValidator(PasswordValidator):

    _error_message: str = _("Password must contain at least %(min_upper)d"
                            " uppercase letter and %(min_lower)d lowercase letter.")
    _help_text: str = _("Your password must contain at least %(min_upper)d"
                        " uppercase letter and %(min_lower)d lowercase letter.")

    def __init__(self, min_upper: int = 1, min_lower: int = 1) -> None:
        self.min_upper = int(min_upper)
        self.min_lower = int(min_lower)

    def validate(self, password: str) -> None:
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
            raise DjangoValidationError(
                self._error_message % {"min_upper": (self.min_upper),
                                       "min_lower": self.min_lower}
            )

    def get_help_text(self) -> None:
        return self._help_text % {'min_upper': (self.min_upper),
                                  'min_lower': self.min_lower}


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
        digits = [c for c in password if c.isdigit()]
        return digits
