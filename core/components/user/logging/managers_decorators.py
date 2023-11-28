import logging
from functools import wraps

from rest_framework_simplejwt.tokens import AccessToken
from user.models import User


def get_user_by_token(access_token):
    decoded_token = AccessToken(access_token)
    user_id = decoded_token['user_id']
    user = _get_user_by_id(user_id)
    return user


def _get_user_by_id(user_id):
    user = User.objects.filter(
        id=user_id).values('id', 'email').first()
    return user


def log_user_deletion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger = logging.getLogger('user_delete')
            user_id = kwargs.get('pk')
            request = kwargs.get('request')

            user = _get_user_by_id(user_id)
            if not user:
                message = "<%(qualname)s> - User %(request_user_id)d trying to delete User %(id)d but this user does not exists. CODE: %(code)d"  # NOQA
                logger.warning(message % {
                    "qualname": func.__qualname__,
                    "request_user_id": request.user.id,
                    "id": int(user_id),
                    "code": 400,
                })
                return func(*args, **kwargs)

            result = func(*args, **kwargs)
            code = result.status_code
            if code == 204:
                # qualname means qualified name and contains string structure like: `class.method`
                info_message = "<%(qualname)s> - User deleted - [id: %(id)d - email: %(email)s] by User [id: %(request_user_id)d]. CODE: %(code)d"  # NOQA

                logger.info(info_message % {
                    "qualname": func.__qualname__,
                    "id": user['id'],
                    "request_user_id": request.user.id,
                    "email": user['email'],
                    "code": code,
                })

            elif code == 400:
                warning_message = "<%(qualname)s> - User %(request_user_id)d trying to delete User %(id)d. CODE: %(code)d"  # NOQA
                logger.warning(warning_message % {
                    "qualname": func.__qualname__,
                    "request_user_id": request.user.id,
                    "id": user['id'],
                    "code": code,
                })

            return result
        except Exception as e:
            error_message = "<%(qualname)s> - Error deleting user: %(e)s. CODE: %(code)d"
            logger.exception(error_message % {
                "qualname": func.__qualname__,
                "method": func.__name__,
                "e": e,
                "code": 400,
            })
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
                info_message = "<%(qualname)s> - User created: [User: %(id)d - %(email)s]"
                logger.info(info_message % {
                    "qualname": func.__qualname__,
                    "id": user['id'],
                    "email": user['email']
                })

            return result
        except Exception as e:
            error_message = "<%(qualname)s> - Error creating user: %(e)s"
            logger.exception(error_message % {
                "qualname": func.__qualname__,
                "e": e,
            })
            raise

    return wrapper
