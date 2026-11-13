from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User with this email already exists"


class UserNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User not found"


class AuthenticationFail(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid email or password"
