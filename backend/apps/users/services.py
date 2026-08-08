from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .exceptions import UserAlreadyExists, AuthenticationFail


User = get_user_model()


def generate_tokens(user) -> dict[str, str]:
    refresh = RefreshToken.for_user(user)
    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }

    return tokens


def create_user(data):
    if User.objects.filter(email=data.get("email")).exists():
        raise UserAlreadyExists

    User.objects.create_user(**data)


def login_user(data):
    user = authenticate(**data)

    if not user:
        raise AuthenticationFail

    tokens = generate_tokens(user)

    return tokens


def logout_user(refresh):
    try:
        token = RefreshToken(refresh)
        token.blacklist()
    except TokenError:
        raise TokenError
