import re

from django.utils.translation import gettext as _

email_errors = {
    "too_many_at_symbols": _("Your email have %(value)d '@' symbols, only 1 allowed."),
    "no_at_symbols": _("Your email doesn\'t have any '@' symbol."),
    "no_character": _("%(object)s should have at least one non-digit character."),
    "start_or_end_with": _("%(object)s can\'t start or end with '%(symbols)s' symbols."),
    "domain_name_no_underscore": _("Domain should not contain an underscore."),
    "not_enough_characters_in_domain_address": _("Domain address should contain at least 2 characters"),
    "email_regex": _("Email contains some unallowed special characters."),
    "domain_parts": _("Domain should contain domain name and domain address splitted by dot"),
    "too_many_symbols_in_a_row": _("You'r %(object)s contains too many special characters in a row")
}


class EmailValidatorService:

    _special_characters = ['-', '_', '.']

    _errors = []

    def __init__(self, email: str = None):
        self.email = email

    def validate(self) -> list | None:
        self._validate_email(self.email)
        return self._return_errors()

    def _validate_email(self, email: str) -> None:
        """
        If email structure is ruined the next validations won't be triggered.
        If email has unallowed characters the next validations won't be triggered.
        """
        name, domain = email.split('@')

        if not self._validate_email_structure(email, name, domain):
            return False

        if not self._validate_email_regex(email):
            return False

        domain_splitted = domain.split('.')

        domain_name = ''.join(domain_splitted[:-1])
        domain_address = domain_splitted[-1]

        self._validate_email_name(name)

        if not self._validate_email_domain(domain):
            return False

        self._validate_email_domain_address(domain_address)
        self._validate_email_domain_name(domain_name)

    def _return_errors(self) -> list | None:
        _errors = list(self._errors)
        self._errors.clear()
        return _errors

    def _validate_email_structure(self, email: str, name: str, domain: str) -> None:
        at_count = email.count('@')
        if at_count > 1:
            self._errors.append(email_errors['too_many_at_symbols'] % {
                "value": at_count
            })
            return False

        if at_count < 1:
            self._errors.append(email_errors['no_at_symbols'])
            return False

        if len(domain.split('.')) < 2:
            self._errors.append(email_errors['domain_parts'])
            return False

        if self._validate_special_symbols_in_a_row(name):
            object_name = _('Email name')
            self._errors.append(email_errors['too_many_symbols_in_a_row'] % {
                "object": object_name
            })
            return False

        if self._validate_special_symbols_in_a_row(domain):
            object_name = _('Email domain')
            self._errors.append(email_errors['too_many_symbols_in_a_row'] % {
                "object": object_name
            })
            return False

        return True

    def _validate_special_symbols_in_a_row(self, string):
        regex_pattern = re.compile(r'(?<=[a-zA-Z])([.-_])\1(?=[a-zA-Z])')
        return bool(regex_pattern.search(string))

    def _validate_email_name(self, name: str) -> None:
        """
        Email name is a part of email before '@'
        """
        object_name = _('Email name')
        self._validate_email_object(name, object_name)

    def _validate_email_domain(self, domain: str) -> None:
        """
        Domain is an end part of email, for example '.com'.

        If domain too short then 'special_symbol_in_domain' validation
        won't be triggered
        """
        object_name = _('Email domain')
        return self._validate_email_object(domain, object_name)

    def _validate_email_domain_address(self, domain_address: str) -> None:
        """
        Domain is an end part of email, for example '.com'.

        If domain too short then 'special_symbol_in_domain' validation
        won't be triggered
        """
        object_name = _('Email domain address')
        self._validate_email_object(domain_address, object_name)
        if len(domain_address) < 2:
            self._errors.append(
                email_errors['not_enough_characters_in_domain_address'])

    def _validate_email_domain_name(self, domain_name: str) -> None:
        """
        Domain name is part of email between '@' and '.com'
        """
        object_name = _('Email domain name')
        self._validate_email_object(domain_name, object_name)

        if '_' in domain_name:
            self._errors.append(email_errors["domain_name_no_underscore"])

    def _validate_email_object(self, object_: str, object_name: str) -> bool:
        """
        Validate email objects. Email objects is a parts of email.

        If email object does not contain any characters the "start_or_end_with"
        validation won't be triggered
        """
        if any(c.isalpha() for c in object_):
            if object_[0] in self._special_characters or object_[-1] in self._special_characters:
                self._errors.append(email_errors['start_or_end_with'] % {
                    "symbols": ['.', '-', '_'],
                    "object": object_name
                })
                return False
            else:
                return True
        else:
            self._errors.append(email_errors['no_character'] % {
                "object": object_name
            })
            return False

    def _validate_email_regex(self, email):
        email_regex = re.compile(
            r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+$')

        if not email_regex.match(email):
            self._errors.append(email_errors['email_regex'])
            return False
        return True
