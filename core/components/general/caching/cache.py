from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import APIException
from functools import wraps


def _get_pk_key(kwargs):
    pk = kwargs.get('pk', '')
    return f"_{pk}" if pk else ''


def _get_admin_key(request: Request):
    user_is_staff = request.user.is_staff
    return '_admin' if user_is_staff else ''


def _get_page_key(request: Request):
    page = request.query_params.get("page")
    return f'_page_{page}' if page else ''


def _get_request(args):
    for arg in args:
        if isinstance(arg, Request):
            return arg


def get_key(cache_key: str, request: Request, kwargs) -> str:
    """Gets full cache key.

    Creates different keys based on user permissions since admins can see
    more fields that default users.

    Args:
        cache_key: string object of cache key.
        args: Unpacked version of `*args`, should contain `request`.
        kwargs: Unpacked version of `**kwargs`.
    Returns:
        String object of full key for cache.
    """

    if not request:
        raise APIException("'Request' variable not provided in request.")

    pk = _get_pk_key(kwargs)
    is_admin = _get_admin_key(request)
    page = _get_page_key(request)

    key = cache_key + is_admin + pk + page
    return key


def cache_method(cache_key: str = None, timeout: int = 60 * 60) -> Response:
    """Caches the result of the function using Django's cache.

    Args:
        cache_key: String object, should be named as `key_method`. For example:\
            `product_type_retrieve`, `product_type_list`, `user_retrieve`.
        timeout: Integer, the duration for which the result should be cached.\
            Time in `seconds`.
    Returns:
        `Response` object with cached data and status code.
    """
    def decorator(func) -> Response:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Response:
            """Generates a cache key.

            Cache key generates based on the cache key, users's permissions
            and PrimaryKey.

            Args:
                *args: Should contain Django's `Request` object named `request`.
                **kwargs: Can contain or not contain `pk`.

            Returns:
                `Response` object with cached data and status code.
            """
            request = _get_request(args)
            key = get_key(cache_key, request, kwargs)

            if request.query_params:
                result = func(*args, **kwargs)
                return Response(result.data, status=result.status_code)

            cached_data = cache.get(key, None)
            if cached_data is not None:
                cached_status_code = cache.get(key + '_status_code')
                return Response(cached_data, status=cached_status_code)

            result = func(*args, **kwargs)
            data = result.data
            status_code = result.status_code
            cache.set(key, data, timeout)
            cache.set(key + '_status_code', status_code, timeout)
            return Response(data, status=status_code)

        return wrapper

    return decorator
