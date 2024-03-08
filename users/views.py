from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, throttle_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.conf import settings

from .thread import generate_activation_email, generate_password_reset_email
from .throttlings import *
from .serializers import *
from .models import User


def get_token_cookie(request):
    """function for getting the refresh token from the cookie"""
    return request.COOKIES.get("refresh") or None


def set_token_cookie(response, refresh_token):
    response.set_cookie(
        "refresh",
        refresh_token,
        max_age=settings.AUTH_COOKIE_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )


@api_view(["POST"])
def user_registration(request):
    """creating new user and send token to their email with expiry of 3 hours"""
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            scheme = "https" if request.is_secure() else "http"
            current_url = f"{scheme}://{request.META['HTTP_HOST']}"
            # sending the activation email using thread
            generate_activation_email(serializer.instance, current_url)
            return Response(
                {"message": "Activation link has been sent to your account"},
                status=status.HTTP_201_CREATED,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@throttle_classes([OncePerDayThrottleForAnonymous])
def activate_account(_request, uidb64, token):
    """activate user account using email url cause token are in the url, if the token isn't expired yet and send the auth token directly"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and default_token_generator.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()

        refresh = RefreshToken.for_user(myuser)
        response = JsonResponse(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "access_token_expiry": settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                "refresh_token_expiry": settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                "message": "Account activated successfully",
            }
        )
        set_token_cookie(response, str(refresh))
        return response

    else:
        return Response(
            {"error": "Invalid token or user"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def request_password_reset(request):
    """Request password reset ask the for an email and send the link of password reset using email"""
    email = request.data.get("email")
    redirect_url = request.data.get("redirect_url")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse(
            {"error": "No user found with this email address"},
            status=status.HTTP_404_NOT_FOUND,
        )

    scheme = "https" if request.is_secure() else "http"
    current_url = f"{scheme}://{request.META['HTTP_HOST']}"
    # sending the reset password email using thread
    generate_password_reset_email(user, redirect_url or current_url)

    return JsonResponse(
        {"message": "Password reset link has been sent to your account"},
        status=status.HTTP_202_ACCEPTED,
    )


@api_view(["POST"])
def reset_password(request, uidb64, token):
    """Reset password asking for the new password and change the password"""
    password = request.data.get("password")

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return JsonResponse(
            {"error": "Invalid user or token"}, status=status.HTTP_400_BAD_REQUEST
        )

    if default_token_generator.check_token(user, token):
        user.password = make_password(password)
        user.save()
        return JsonResponse(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )
    else:
        return JsonResponse(
            {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        """This is the simple login view expect email password and send the token"""
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = response.data.get("refresh")

            set_token_cookie(response, refresh_token)
            response.data["access_token_expiry"] = settings.SIMPLE_JWT[
                "ACCESS_TOKEN_LIFETIME"
            ]
            response.data["refresh_token_expiry"] = settings.SIMPLE_JWT[
                "REFRESH_TOKEN_LIFETIME"
            ]

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        """This is the simple renewel token view ask for refresh token and send new token"""
        refresh_token = get_token_cookie(request)

        if refresh_token:
            request.data["refresh"] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = response.data.get("refresh")
            set_token_cookie(response, refresh_token)

        response.data["access_token_expiry"] = settings.SIMPLE_JWT[
            "ACCESS_TOKEN_LIFETIME"
        ]
        response.data["refresh_token_expiry"] = settings.SIMPLE_JWT[
            "REFRESH_TOKEN_LIFETIME"
        ]

        return response
