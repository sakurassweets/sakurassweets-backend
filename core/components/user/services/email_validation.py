import re
from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError as DjangoValidationError

from django.utils.translation import gettext as _


class BaseEmailValidator(ABC):
    @abstractmethod
    def validate(self, *args, **kwargs) -> None:
        pass


class EmailValidator(BaseEmailValidator):
    @abstractmethod
    def get_help_text(self) -> str:
        pass


class EmailValidatorService(BaseEmailValidator):
    __slots__ = ['email']
    _errors: list = []

    def __init__(self, email: str = None):
        self.email = email

    def validate(self) -> list | None:
        self._validate_email()
        if len(self._errors) > 0:
            return self._return_errors()

    def _validate_email(self) -> None:
        """
        If email structure is ruined the next validations won't be triggered.
        If email has unallowed characters the next validations won't be triggered.
        """
        validators = self.__default_validators

        if not validators:
            return False

        for validator in validators:
            self._validate_or_error(validator)

    def _validate_or_error(self, validator) -> str:
        try:
            validator.validate()
        except DjangoValidationError as error:
            error = str(error)
            self._errors.append(str(error)[2:-2])

    def _return_errors(self) -> list | None:
        _errors = list(self._errors)
        self._errors.clear()
        return _errors

    def __validate_email_structure(self, email: str) -> None:
        """
        Validates email structure before starting next validations cause
        they depends on email structure and if it's ruined validation can be
        ruined as well
        """
        validator = EmailStructureValidator(email)
        try:
            validator.validate()
            return True
        except DjangoValidationError as error:
            error = str(error)
            self._errors.append(str(error)[2:-2])
            return False

    @staticmethod
    def __get_name_and_domain(email: str) -> tuple[str, str]:
        name, domain = email.split('@')
        return name, domain

    @staticmethod
    def __get_names() -> tuple[str, str]:
        """
        Get names of variables that used in exception handling
        """
        email_name = _('Email name')
        domain_name = _('Email domain')
        return email_name, domain_name

    @staticmethod
    def __get_domain_name_and_address(domain: str) -> tuple[str, str]:
        """
        Get domain name and domain address that contains in domain.

        ...@<domain_name>.<domain_address>
        """
        domain_splitted = domain.split('.')
        domain_name = ''.join(domain_splitted[:-1])
        domain_address = domain_splitted[-1]
        return domain_name, domain_address

    @property
    def __default_validators(self) -> list:
        """
        Returns default validators list after validating email structure
        """
        if not self.__validate_email_structure(self.email):
            return False

        name, domain = self.__get_name_and_domain(self.email)
        email_name, domain_name = self.__get_names()
        domain_name_string, domain_address = self.__get_domain_name_and_address(
            domain=domain
        )

        default_validators = [
            EmailStartOrEndWithValidator(
                name, email_name
            ),
            EmailStartOrEndWithValidator(
                domain, domain_name
            ),
            EmailDomainAddressValidator(domain_address),
            EmailDomainNameValidator(domain_name_string),
            EmailRegexValidator(self.email),
        ]
        return default_validators


class EmailDomainNameValidator(EmailValidator):
    """
    Validates if domain name start ot end with special characters
    and if domain name has underscore

    Structure: <email_name>@<domain_name>.<domain_address>
    """
    __slots__ = ['domain_name']
    _domain_name_underscore = _("Domain should not contain an underscore.")

    def __init__(self, domain_name: str) -> None:
        self.domain_name = domain_name

    def validate(self) -> None:
        self._validate_domain_name_object()
        self._validate_domain_name_underscore()

    def get_help_text(self) -> str:
        return super().get_help_text()

    def _validate_domain_name_object(self) -> None:
        object_name = _("Email domain name")
        validator = EmailStartOrEndWithValidator(
            self.domain_name, object_name)
        validator.validate()

    def _validate_domain_name_underscore(self):
        if '_' in self.domain_name:
            raise DjangoValidationError(
                self._domain_name_underscore
            )


class EmailRegexValidator(EmailValidator):
    """
    Validates if email has any unallowed special characters by RegEx
    """
    __slots__ = ['email', 'email_regex']
    _error_message: str = _(
        "Email contains some unallowed special characters.")
    _email_regex: str = re.compile(
        r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+$')
    _help_text: str = _(
        "Email should not contain unallowed special characters.")

    def __init__(self, email: str, email_regex: str = None) -> None:
        self.email = email
        if email_regex is not None:
            self._email_regex = email_regex

    def validate(self) -> None:
        if not self._email_regex.match(self.email):
            raise DjangoValidationError(self._error_message)

    def get_help_text(self) -> str:
        return self._help_text


class EmailDomainAddressValidator(EmailValidator):
    """
    Validates that:
    - domain address does not contain any special characters
    - domain address does not contain any digits
    - domain address longer than 2 characters and shorter than 6 characters

    Structure: <email_name>@<domain_name>.<domain_address>
    """
    __slots__ = ['domain_address']
    _domain_address_special_symbols: str = _(
        "Domain address should not contain any special characters"
    )
    _domain_address_digits: str = _(
        "Domain address should not contain any digits"
    )
    _not_enough_characters_in_domain_address: str = _(
        "Domain address should contain at least 2 characters"
    )
    _too_many_characters_in_domain_address: str = _(
        "Domain address should contain maximum 6 characters"
    )
    _help_text: str = _(
        "Email domain address should not contain special characters, any digits, \
should contain at least 2 characters and maximum 6 characters"
    )
    _object_name: str = _('Email domain address')
    _special_characters: list = ['-', '_', '.']

    def __init__(self, domain_address: str) -> None:
        self.domain_address = domain_address

    def validate(self) -> None:
        self._validate_domain_address()

    def get_help_text(self) -> str:
        return self._help_text

    def _validate_domain_address(self) -> None:
        validations_list = self._validations
        for validation in validations_list:
            validation()

    @property
    def _validations(self) -> list:
        """
        List of validators for iteration
        """
        validations_list = [
            self.__validate_domain_address_digits,
            self.__validate_domain_address_length,
            self.__validate_domain_address_special_characters
        ]
        return validations_list

    def __validate_domain_address_special_characters(self) -> None:
        if any(c in self._special_characters for c in self.domain_address):
            raise DjangoValidationError(
                self._domain_address_special_symbols
            )

    def __validate_domain_address_digits(self) -> None:
        if any(c.isdigit() for c in self.domain_address):
            raise DjangoValidationError(
                self._domain_address_digits
            )

    def __validate_domain_address_length(self) -> None:
        if len(self.domain_address) < 2:
            raise DjangoValidationError(
                self._not_enough_characters_in_domain_address
            )
        if len(self.domain_address) > 6:
            raise DjangoValidationError(
                self._too_many_characters_in_domain_address
            )


class EmailStartOrEndWithValidator(EmailValidator):
    """
    Validates email objects that:
    - object didn't start or end with special characters
    - object have at least one non-digit character

    Email objects is a objects from general email structure:
    - <email_name>@<domain_name>.<domain_address>

    Domain contains domain name and address
    """
    __slots__ = ['string', 'object_name']
    _error_message: str = _(
        "%(object)s can\'t start or end with '%(symbols)s' symbols.")
    _no_characters_error: str = _(
        "%(object)s should have at least one non-digit character.")
    _help_text: str = _(
        "%(object)s shouldn't start or end with '%(symbols)s' symbols.")
    _special_characters: list = ['-', '_', '.']

    def __init__(self, string: str, object_name: str) -> None:
        self.string = string
        self.object_name = object_name

    def validate(self) -> None:
        self._validate_characters_in_string()
        self._validate_start_or_end_with_special_character()

    def get_help_text(self) -> str:
        return self._help_text % {
            "object": self.object_name,
            "symbols": self._special_characters
        }

    def _validate_characters_in_string(self) -> None:
        if not any(c.isalpha() for c in self.string):
            raise DjangoValidationError(
                self._no_characters_error % {
                    "object": self.object_name,
                }
            )

    def _validate_start_or_end_with_special_character(self) -> None:
        if self.string[0] in self._special_characters or self.string[-1] in self._special_characters:
            raise DjangoValidationError(
                self._error_message % {
                    "object": self.object_name,
                    "symbols": self._special_characters
                }
            )


class EmailStructureValidator(EmailValidator):
    """
    Validates email structure. Validates that:
    - Email have only one '@' symbol
    - Domain contains domain_name and domain_address splitted by dot
    - Email parts didn't have 2 or more special characters in a row
    """
    __slots__ = ['email']
    too_many_at_error: str = _(
        "Your email have %(value)d '@' symbols, only 1 allowed."
    )
    no_at_error: str = _(
        "Your email doesn\'t have any '@' symbol."
    )
    domain_parts_error: str = _(
        "Domain should contain domain name and domain address splitted by dot"
    )
    too_many_symbols_in_a_row: str = _(
        "You'r %(object)s contains too many special characters in a row"
    )
    _help_text: str = _("Your email should have only 1 '@' symbol")

    def __init__(self, email: str) -> None:
        self.email = email

    def validate(self) -> None:
        self._validate_at_symbols_amount()
        name, domain = self.email.split('@')
        self._validate_domain_structure(domain)
        self._validate_name_special_symbols_in_a_row(name)
        self._validate_domain_special_symbols_in_a_row(domain)

    def get_help_text(self) -> str:
        return self._help_text

    def _validate_at_symbols_amount(self) -> None:

        at_count = self.email.count('@')
        if at_count > 1:
            raise DjangoValidationError(
                self.too_many_at_error % {"value": at_count}
            )
        if at_count < 1:
            raise DjangoValidationError(
                self.no_at_error
            )

    def _validate_domain_structure(self, domain: str) -> None:

        if len(domain.split('.')) < 2:
            raise DjangoValidationError(
                self.domain_parts_error
            )

    def _validate_name_special_symbols_in_a_row(self, name: str) -> None:
        if self.__validate_special_symbols_in_a_row(name):
            object_name = _('Email name')
            raise DjangoValidationError(
                self.too_many_symbols_in_a_row % {
                    "object": object_name
                }
            )

    def _validate_domain_special_symbols_in_a_row(self, domain: str) -> None:
        if self.__validate_special_symbols_in_a_row(domain):
            object_name = _('Email domain')
            raise DjangoValidationError(
                self.too_many_symbols_in_a_row % {
                    "object": object_name
                }
            )

    def __validate_special_symbols_in_a_row(self, string: str) -> bool:
        regex_pattern = re.compile(r'(?<=[a-zA-Z])([.-_])\1(?=[a-zA-Z])')
        return bool(regex_pattern.search(string))
