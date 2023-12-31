from django.core.cache import cache
from rest_framework.response import Response
from functools import wraps


def cache_user_method(cache_key=None, timeout=60 * 60):
    """
    A decorator that caches the result of the function using Django's cache.

    Input:
    - cache_key: !!! Should be named as `key_method` for example `product_type_retrieve` !!!
    - timeout: The duration for which the result should be cached. Time in `seconds`, can be specified as `60 * 60 * 12 (12 hours)`

    Usage:
    @cache_user_method(timeout=60)  # Cache for 60 seconds
    def your_function_or_method(*args, **kwargs):
        # Your logic here
        return result
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a cache key based on the function qualname and its arguments
            pk = kwargs.get('pk', '')
            pk = f"_{pk}" if pk else ''
            key = f"{cache_key + pk}"
            # Check if the data is already in the cache
            cached_data = cache.get(key)
            if cached_data is not None:
                cached_status_code = cache.get(key + '_status_code')
                return Response(cached_data, status=cached_status_code)

            # If not, compute the data and store it in the cache
            result = func(*args, **kwargs)
            data = result.data
            status_code = result.status_code
            cache.set(key, data, timeout)
            cache.set(key + '_status_code', status_code, timeout)
            return Response(data, status=status_code)

        return wrapper

    return decorator
