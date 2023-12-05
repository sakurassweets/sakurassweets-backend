import logging
from functools import wraps

from rest_framework_simplejwt.tokens import AccessToken
from user.models import User


def get_user_by_token(access_token: str) -> User:
    decoded_token = AccessToken(access_token)
    user_id = decoded_token['user_id']
    user = _get_user_by_id(user_id)
    return user


def _get_user_by_id(user_id: int | str) -> User:
    """
    This method get's only `id` and `email` from User model.
    """
    user = User.objects.filter(
        id=user_id).values('id', 'email').first()
    return user


def log_user_update(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger = logging.getLogger('user_update')
            user_id = kwargs.get('pk')
            request = kwargs.get('request')

            user = _get_user_by_id(user_id)
            if not user:
                _message = "<%(qualname)s> - User %(request_user_id)s trying to update User [id: %(id)s] but this user does not exists. CODE: %(code)d"  # NOQA
                warning_message = _message % {
                    "qualname": func.__qualname__,
                    "request_user_id": request.user.id,
                    "id": int(user_id),
                    "code": 400,
                }
                logger.warning(warning_message)
                return func(*args, **kwargs)

            result = func(*args, **kwargs)
            code = result.status_code
            if code == 200:
                # qualname means qualified name and contains string structure like: `class.method`
                _message = "<%(qualname)s> - User [id: %(id)s - email: %(email)s] updated by User [id: %(request_user_id)s]. changes: [%(changes)s] CODE: %(code)d"  # NOQA

                info_message = _message % {
                    "qualname": func.__qualname__,
                    "id": user['id'],
                    "request_user_id": request.user.id,
                    "email": user['email'],
                    "code": code,
                    "changes": result.data['data'].keys()
                }
                logger.info(info_message)

            elif code == 400:
                _message = "<%(qualname)s> - User [id: %(request_user_id)s] trying to update User [id: %(id)s]. CODE: %(code)d"  # NOQA
                warning_message = _message % {
                    "qualname": func.__qualname__,
                    "request_user_id": request.user.id,
                    "id": user['id'],
                    "code": code,
                }
                logger.warning(warning_message)

            return result
        except Exception as e:
            _message = "<%(qualname)s> - Error deleting user: %(e)s. CODE: %(code)d"
            error_message = _message % {
                "qualname": func.__qualname__,
                "method": func.__name__,
                "e": e,
                "code": 400,
            }
            logger.exception(error_message)
            raise

    return wrapper


def log_user_deletion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger = logging.getLogger('user_delete')
            user_id = kwargs.get('pk')
            request = kwargs.get('request')

            user = _get_user_by_id(user_id)
            if not user:
                _message = "<%(qualname)s> - User [id: %(request_user_id)s] trying to delete User [id: %(id)s] but this user does not exists. CODE: %(code)d"  # NOQA
                warning_message = _message % {
                    "qualname": func.__qualname__,
                    "request_user_id": request.user.id,
                    "id": int(user_id),
                    "code": 400,
                }
                logger.warning(warning_message)
                return func(*args, **kwargs)

            result = func(*args, **kwargs)
            code = result.status_code
            if code == 204:
                # qualname means qualified name and contains string structure like: `class.method`
                _message = "<%(qualname)s> - User [id: %(id)s - email: %(email)s] deleted by User [id: %(request_user_id)s]. CODE: %(code)d"  # NOQA

                info_message = _message % {
                    "qualname": func.__qualname__,
                    "id": user['id'],
                    "request_user_id": request.user.id,
                    "email": user['email'],
                    "code": code,
                }
                logger.info(info_message)

            elif code == 400:
                _message = "<%(qualname)s> - User [id: %(request_user_id)s] trying to delete User [id: %(id)s]. CODE: %(code)d"  # NOQA
                warning_message = _message % {
                    "qualname": func.__qualname__,
                    "request_user_id": request.user.id,
                    "id": user['id'],
                    "code": code,
                }
                logger.warning(warning_message)

            return result
        except Exception as e:
            _message = "<%(qualname)s> - Error deleting User [id: %(id)s]: %(e)s. CODE: %(code)d"  # NOQA
            error_message = _message % {
                "qualname": func.__qualname__,
                "id": user_id if user_id else 'undefined',
                "e": e,
                "code": 400,
            }
            logger.exception(error_message)
            raise

    return wrapper


def log_user_creation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger = logging.getLogger('user_create')
            result = func(*args, **kwargs)
            access_token = result.get('access')
            user = get_user_by_token(access_token)
            if user:
                info_message = "<%(qualname)s> - User created: [User: %(id)s - %(email)s]"
                logger.info(info_message % {
                    "qualname": func.__qualname__,
                    "id": user['id'],
                    "email": user['email']
                })

            return result
        except Exception as e:
            _message = "<%(qualname)s> - Error creating user: %(e)s"
            error_message = _message % {
                "qualname": func.__qualname__,
                "e": e,
            }
            logger.exception(error_message)
            raise

    return wrapper
