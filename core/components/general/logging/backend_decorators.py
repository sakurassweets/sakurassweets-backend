import logging
from functools import wraps

from django.db import connection


def log_db_query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('django')
        result = func(*args, **kwargs)
        logger.info("\n" + "#" * 50 + f" 'START {func.__name__}' " + "#" * 120)  # NOQA
        for q in connection.queries:
            logger.info(q)
        logger.info("\n" + "#" * 50 + f" 'END {func.__name__}' " + "#" * 120)  # NOQA

        return result
    return wrapper
