from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import (RegisterSerializer, LoginSerializer)
from .services import create_user, login_user, logout_user


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_user(serializer.validated_data)

        return Response(
            {"message": "User successfully created"},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = login_user(serializer.validated_data)

        response = Response(
            {"access": tokens["access"]},
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            "refresh_token",
            tokens["refresh"],
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60
        )

        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]

    logout_response = Response(
        {'message': 'Successfully logged out'},
        status=status.HTTP_200_OK
    )

    def post(self, request):
        refresh = request.COOKIES.get("refresh_token")

        if not refresh:
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK
            )

        try:
            logout_user(refresh)
        except TokenError:
            pass
        finally:
            response = Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK
            )
            response.delete_cookie("refresh_token")
            return response


class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get(
            "refresh_token") or request.data.get("refresh")

        if not refresh:
            raise InvalidToken("No refresh token provided")

        request.data["refresh"] = refresh
        response = super().post(request, *args, **kwargs)

        if response.data.get("refresh"):
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=7 * 24 * 60 * 60
            )
            del response.data["refresh"]

        return response
