from typing import Literal
# variables for password validation
MIN_PASSWORD_LENGTH: int = 8
MAX_PASSWORD_LENGTH: int = 40
MAX_SIMILARITY: float = 0.55
MIN_DIGITS: int = 1
# required fields in input for user update
REQUIRED_UPDATE_FIELDS: list = ['email']
SAFE_ACTIONS: Literal['create', 'list', 'retrieve'] = [
    'create',
    'list',
    'retrieve'
]
PRIVATE_ACTIONS: Literal['update', 'partial_update', 'destroy'] = [
    'update',
    'partial_update',
    'destroy'
]


def constants_list_for_password_validation() -> dict:
    """
    returns mapping of constants for password validation
    """
    constants: dict = {
        "min_len": MIN_PASSWORD_LENGTH,
        "max_len": MAX_PASSWORD_LENGTH,
        "max_similarity": MAX_SIMILARITY,
        "min_digits": MIN_DIGITS
    }
    return constants


PASSWORD_CONSTANTS: dict = constants_list_for_password_validation()
