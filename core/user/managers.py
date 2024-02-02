from typing import Literal
import copy

from django.utils.translation import gettext as _
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from celery.result import AsyncResult

from components.user.logging.managers_decorators import (
    log_user_creation,
    log_user_deletion,
    log_user_update,
)
from components.user.validators import UserValidator, PasswordValidator, EmailValidator
from components.user import constants

from user.tasks import hash_password, send_welcome_email
from user.models import User


class UserCreateManager:
    """Manager that provides user creation.

    Provides user creation after validation. User creates with hashed
    password. Also this manager sends welcome email to user email.
    """
    @classmethod
    @log_user_creation
    def create_user(cls, serializer: Serializer) -> dict:
        """Provides user creating after validation and sending welcome email.

        Args:
            serializer: Serializer for user model. `Serializer` instance with
                data from request.

        Returns:
            dictionary that contains user's access token and refresh token.
            For example:

            {"refresh": "refresh_token_here", "access": "access_token_here"}

        Raises:
            ValidationError if validation failed.
        """
        email, password = cls._get_user_data(serializer)
        hash_result = hash_password.delay(password)
        user = cls._create_user(password, email)
        cls._set_user_properties(hash_result, user)
        context = cls._build_context(user)
        cls._send_welcome_email(user)
        return context

    @staticmethod
    def _get_user_data(serializer: Serializer) -> tuple[str, str]:
        """Gets user data using serializer

        Args:
            serializer: Serializer for user model to validate data.
                `Serializer` instance with data from request.

        Returns:
            tuple of strings with email, password.
        """
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        return email, password

    @staticmethod
    def _create_user(password: str, email: str) -> User:
        """Creates user after validation by `UserValidator`.

        Args:
            password: string object of user password.
            email: string object of user email.

        Returns:
            Newly created user object, `User` instance.

        Raises:
            ValidationError if validation failed.
        """
        UserValidator.validate(password, email)
        return User.objects.create_user(password=password, email=email)

    @staticmethod
    def _build_context(user: User) -> dict:
        """Gets tokens for created user.

        Args:
            user: object of user, `User` instance.

        Returns:
            dictionary that contains user's access token and refresh token.
            For example:

            {"refresh": "refresh_token_here", "access": "access_token_here"}
        """
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        context = {
            'access': str(access_token),
            'refresh': str(refresh_token)
        }
        return context

    @staticmethod
    def _set_user_properties(hash_result: str, user: User) -> None:
        """Sets hashed password for user and updates user last login time

        Args:
            hash_result: string object user hashed password.
            user: object of user, `User` instance.
        """
        async_result = AsyncResult(hash_result.task_id)
        async_result.wait(interval=0.01)

        password = hash_result.result
        User.objects.filter(id=user.id).update(
            last_login=timezone.now(),
            password=password
        )

    @staticmethod
    def _send_welcome_email(user: User) -> None:
        data = {
            'user_email': user.email
        }
        send_welcome_email.delay(data)


class UserUpdateManager:
    """Manager that provides user updating.

    Provides user updating after validation.
    User can be updated in several ways.

    Update types:
        partial_update: Update by PATCH method, updates any of fields.
        updated: Update by PUT method, takes all fields to perform update.
    Update ways:
        Updated all fields but don't set new password.
        Update only password by sending new_password.
    """
    _previous_email_err: str = _("You'r email can't be same as previous one.")
    _no_permission_error: str = _("You have no permission to update this user")
    _new_password_error: str = _("New password can't be the same as old one.")
    _empty_data_error: str = _("You should send at least any data.")
    _empty_field_error: str = _("This field can't be empty.")
    _required_field_error: str = _("This field is required")

    _required_fields: list = constants.REQUIRED_UPDATE_FIELDS
    _updated_data: dict = {}

    def partial_update(self, *, request: Request, serializer: Serializer, pk: int) -> Response:
        """Provides partial update of user, PATCH method.

        Args:
            request: KeyWord arg only, a DRF's `Request` object.
            serializer: KeyWord arg only, Serializer for user model
                to validate data. `Serializer` instance with data from request.
            pk: integer, primary key (id) of user that being updated.

        Returns:
            `Response` object with json body (info or errors) and HTTP
            status code. Codes: 200, 400.
        """
        response = self._update_and_return_response(
            request=request,
            serializer=serializer,
            pk=pk,
            partial=True
        )
        self._updated_data.clear()
        return response

    def update(self, *, request: Request, serializer: Serializer, pk: int) -> Response:
        """Provides update of user, PUT method.

        Args:
            request: KeyWord arg only, a DRF's `Request` object.
            serializer: KeyWord arg only, Serializer for user model
                to validate data. `Serializer` instance with data from request.
            pk: integer, primary key (id) of user that being updated.

        Returns:
            `Response` object with json body (info or errors) and HTTP
            status code. Codes: 200, 400.
        """
        response = self._update_and_return_response(request, serializer, pk)
        self._updated_data.clear()
        return response

    def perform_update(self, user: User, data: dict) -> None:
        """Performs update for fields if they updated

        save() method wouldn't be called if at least one field wouldn't be updated.

        Args:
            user: user that being changed, `User` instance.
            data: a dictionary with user changed data.
        """
        for key, value in data.items():
            if key == 'password':
                continue
            if value != getattr(user, key):
                setattr(user, key, value)
                self._updated_data[key] = value

        if len(self._updated_data.items()) > 0:
            user.save()

    def _update_user(self,
                     request_user: User,
                     user: User,
                     data: dict,
                     serializer: Serializer,) -> tuple[dict[str, str], Literal[200, 400]]:
        """Update a user.

        Args:
            request_user: user that made request, `User` instance.
            user: user that being updated, `User` instance.
            data: A dictionary with user changed data.
            serializer: Serializer for user model to validate data.
                `Serializer` instance with data from the request.

        Returns:
            A tuple containing a dictionary with information about the update
            and an HTTP status code. Codes: 200, 400.
        """
        response = self._check_permission(request_user, user)
        if isinstance(response, tuple):
            response, status_ = response
            return response, status_

        validated_data_response = self._validate_data(user, data, serializer)
        if isinstance(validated_data_response, tuple):
            message, status_ = validated_data_response
            if message:
                return message, status_

        # if we get new password we change only password and doesn't care about other fields
        if 'new_password' in data:
            new_password = data.get('new_password')
            response, status_ = self._change_password(user, new_password)
            return response, status_
        else:
            self.perform_update(user, data)

        return self._updated_data, status.HTTP_200_OK

    @log_user_update
    def _update_and_return_response(self,
                                    request: Request,
                                    serializer: Serializer,
                                    pk: int,
                                    partial: bool = False) -> Response:
        """Provides user updating.

        Args:
            request: KeyWord arg only, a DRF's `Request` object.
            serializer: KeyWord arg only, Serializer for user model
                to validate data. `Serializer` instance with data from request.
            pk: integer, primary key (id) of user that being updated.
            partial: boolean, if True - user updating with partial_update
                method (PATCH)
        Returns:
            `Response` object with json body (info or errors) and HTTP
            status code. Codes: 200, 400.
        """
        user = User.objects.get(id=pk)
        request_user = request.user
        data = request.data

        if response_empty := self._validate_empty_fields(data):
            return Response({"detail": response_empty},
                            status=status.HTTP_400_BAD_REQUEST)

        if not partial:
            if result := self._validate_partial_update(user, data):
                return Response({"detail": result},
                                status=status.HTTP_400_BAD_REQUEST)

        data_, status_ = self._update_user(request_user=request_user,
                                           user=user,
                                           data=data,
                                           serializer=serializer)
        data = copy.deepcopy(data_)
        if 'detail' in data:
            return Response(data, status_)

        return Response({"data": data}, status_)

    def _check_permission(self,
                          request_user: User,
                          user: User) -> tuple[dict[str, str], Literal[400]] | Literal[False]:
        """Checks permission to update user.

        If user that send request trying update other user he should be superuser.

        Args:
            requset_user: user that made request, `User` instance.
            user: user that being changed, `User` instance.

        Returns:
            If check fails: A tuple containing a dictionary with errors
            of checking and an HTTP status code. Codes: 400.

            If check passes: Just returns `False`.
        """
        if request_user.id == user.id or request_user.is_superuser:
            return False
        else:
            return {"detail": self._no_permission_error}, status.HTTP_400_BAD_REQUEST

    def _change_password(self, user: User, new_password: str) -> tuple[dict[str, str], Literal[200, 400]]:
        """Changes password for user.

        Args:
            user: user that being changed, `User` instance.
            new_password: string object of new password for user.

        Returns:
            A tuple containing a dictionary with information about the
            updated data or with errors and an HTTP status code.
            Codes: 200, 400.
        """
        user.password = new_password
        user.save()
        self._updated_data['new_password'] = user.password
        return self._updated_data, status.HTTP_200_OK

    def _validate_data(self,
                       user: User,
                       data: dict,
                       serializer: Serializer) -> tuple[dict[str, str], Literal[400]] | None:
        """Validates data using serializer.

        Args:
            user: user that being changed, `User` instance.
            data: a dictionary with user changed data.
            serializer: Serializer for user model. `Serializer` instance with
                data from request.

        Returns:
            If fails: A tuple containing a dictionary with errors and an
            HTTP status code. Codes: 400.
            If passes: Just returns False.
        """
        if new_password := data.get('new_password'):
            response = self._validate_new_password(
                new_password=new_password,
                user=user
            )
            if response is not None:
                return {"detail": response}, status.HTTP_400_BAD_REQUEST

            return None

        user_email = user.email
        request_email = data.get('email')

        if result := self._validate_new_email(user_email, request_email):
            return {"detail": result}, status.HTTP_400_BAD_REQUEST

        try:
            serializer = serializer(data=data)
            serializer.is_valid(raise_exception=True)
            return None
        except ValidationError as error:
            # avoid error raised by unique values
            if user_email == request_email:
                return None
            else:
                return {"detail": error}, status.HTTP_400_BAD_REQUEST

    def _validate_empty_fields(self, data: dict) -> dict[str, str] | None:
        """Validates empty fields.

        If any of fields is empty the error will be added to errors list

        Args:
            data: A dictionary with user changed data.

        Returns:
            Dictionary that contains information about errors occured.
            For example:

            {"email": "This field can't be empty."}

            If validate is succesful then will be returned `None`.
        """
        errors: dict = {}

        if not data:
            errors["error"] = self._empty_data_error
        else:
            for key, value in data.items():
                if value is None:
                    errors[key] = self._empty_field_error

        return errors if errors else None

    def _validate_required_fields(self, data: dict) -> dict[str, str] | None:
        """Validates required fields for PUT method

        If any of required fileds is not in data, the error
        will be added to errors list

        Args:
            data: A dictionary with user changed data.

        Returns:
            Dictionary that contains information about errors occured.
            For example:

            {"email": "This field is required"}

            If validate is succesful then will be returned `None`.
        """
        errors: dict = {}
        for field in self._required_fields:
            if field not in data:
                errors[field] = self._required_field_error

        return errors if errors else None

    def _validate_partial_update(self, user: User, data: dict) -> Response | None:
        if response_required := self._validate_required_fields(data):
            return response_required

        if validation := self._validate_password(user=user,
                                                 password=data.get('password'),
                                                 is_password_new=False):
            return validation

        return None

    def _validate_new_email(self, user_email: str, request_email: str) -> dict[str, str] | None:
        """Validate new password for user.

        Args:
            user_email: string object of email from user that made request.
            request_email: string object of email from request.
                request_email means the email to which the existing one
                will be changed.

        Returns:
            If fails: A dictionary with errors.
            If passes: Just returns None.
        """

        if request_email:
            result = EmailValidator.validate(request_email)
            if user_email == request_email:
                return {"email": self._previous_email_err}
        else:
            result = None

        if result:
            return {"email": result}

        return None

    def _validate_password(self, user: User, password: str, is_password_new: bool) -> dict[str, str] | None:
        check_password = user.check_password(password)

        if check_password:
            if is_password_new:
                return {"new_password": self._new_password_error}
            else:
                return None
        else:
            if not is_password_new:
                return {"password": "You provided wrong password, please try again."}

    def _validate_new_password(self, user: User, new_password: str) -> dict[str, str] | None:
        """Validate new password for user.

        Args:
            user: user that being changed, `User` instance.
            new_password: string object of new password for user.

        Returns:
            If fails: A dictionary with errors.
            If passes: Just returns None.
        """
        if validation := self._validate_password(user, new_password, True):
            return validation

        if result := PasswordValidator.validate(new_password, user):
            return {"new_password": result}

        return None


class UserDeleteManager:

    _error_message = _("Something went wrong during user delition")
    _permission_error_message = _("You have no permission to delete this user")

    @log_user_deletion
    def delete(self, *, request: Request, pk: int) -> Response:
        """Deletes user by primary key.

        Args:
            request: KeyWord arg only, a DRF's `Request` object.
            pk: KeyWord arg only, integer, primary key (id) of user
                that being deleted.

        Returns:
            `Response` object with json body and HTTP status code.
                Codes: 204, 400.
        """
        user = request.user
        if not self._check_permission(user, pk):
            return Response({
                "detail": self._permission_error_message
            }, status=status.HTTP_400_BAD_REQUEST)

        self._delete_user(pk)
        if self._check_user_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            "detail": self._error_message
        }, status=status.HTTP_400_BAD_REQUEST)

    def _delete_user(self, pk: int) -> None:
        user = User.objects.get(id=pk)
        user.delete()

    def _check_permission(self, user: User, pk: id) -> bool:
        """Checks permission to delete user.

        Args:
            user: user that requested delition, `User` instance.
            pk: integer, primary key (id) of user
                that being deleted.

        Returns:
            `True` if user has permission and `False` is doesn't.
        """
        if not user.id:
            return False

        if int(user.id) == int(pk) or user.is_superuser:
            return True

        return False

    @staticmethod
    def _check_user_deleted(pk: int) -> bool:
        try:
            User.objects.get(id=pk)
            return False
        except User.DoesNotExist:
            return True
