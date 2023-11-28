import copy
from custom_logging.user.managers_logger import initialize_user_managers_logger
from custom_logging.django.django_logger import initialize_django_logger
from custom_logging.django.db_logger import initialize_db_logger

django_logger = initialize_django_logger()
user_managers_logger = initialize_user_managers_logger()
db_logger = initialize_db_logger()

loggers = [django_logger, user_managers_logger, db_logger]
keys = ['formatters', 'handlers', 'loggers']


def initialize_loggers():
    combined_logger = copy.deepcopy(loggers[0])

    for logger in loggers[1:]:
        combined_logger["formatters"].update(logger.get("formatters", {}))
        combined_logger["handlers"].update(logger.get("handlers", {}))
        combined_logger["loggers"].update(logger.get("loggers", {}))

    return combined_logger
