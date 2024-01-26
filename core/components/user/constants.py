MIN_PASSWORD_LENGTH: int = 8
MAX_PASSWORD_LENGTH: int = 40
MAX_SIMILARITY: float = 0.55
MIN_DIGITS: int = 1
# required fields in input for user update by PUT method
REQUIRED_UPDATE_FIELDS: list = ['email', 'password']
CACHE_TIMEOUT = 60 * 60


def constants_list_for_password_validation() -> dict[str, int]:

    constants: dict = {
        "min_len": MIN_PASSWORD_LENGTH,
        "max_len": MAX_PASSWORD_LENGTH,
        "max_similarity": MAX_SIMILARITY,
        "min_digits": MIN_DIGITS
    }
    return constants


PASSWORD_CONSTANTS = constants_list_for_password_validation()
