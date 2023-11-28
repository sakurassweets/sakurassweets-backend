import logging
from functools import wraps

from django.db import connection


def log_db_query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('django')
        result = func(*args, **kwargs)
        for query in connection.queries:
            message = query['sql']
            logger.info(message)
        return result
    return wrapper
