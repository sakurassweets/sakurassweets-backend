import copy
from typing import Any

from custom_logging.user.managers_logger import initialize_user_managers_logger
from custom_logging.django.backend_logger import initialize_backend_logger

user_managers_logger = initialize_user_managers_logger()
backend_logger = initialize_backend_logger()

loggers = [backend_logger, user_managers_logger]
keys = ['formatters', 'handlers', 'loggers']


def initialize_loggers() -> dict[str, Any]:
    """Initializes Django logger.

    This file provides initializing of Django's logger by collecting other
    logger pieces. First logger in list always should be a backend logger
    because it provides `version` and `disable_existing_loggers` fields
    which is writing on 'top' of logger dictionary
    """
    combined_logger = copy.deepcopy(loggers[0])

    for logger in loggers[1:]:
        combined_logger["formatters"].update(logger.get("formatters", {}))
        combined_logger["handlers"].update(logger.get("handlers", {}))
        combined_logger["loggers"].update(logger.get("loggers", {}))

    return combined_logger
