MIN_PASSWORD_LENGTH: int = 8
MAX_PASSWORD_LENGTH: int = 40
MAX_SIMILARITY: float = 0.55
MIN_DIGITS: int = 1


def constants_list_for_password_validation() -> dict:
    constants: dict = {
        "min_len": MIN_PASSWORD_LENGTH,
        "max_len": MAX_PASSWORD_LENGTH,
        "max_similarity": MAX_SIMILARITY,
        "min_digits": MIN_DIGITS
    }
    return constants
