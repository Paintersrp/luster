from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, exceptions
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.response import Response
from django.db import IntegrityError
from .models import User, TokenBlacklist
from .serializers import *
import json
import jwt
from rest_framework.decorators import permission_classes
import datetime
from django.core.exceptions import ObjectDoesNotExist
from api.sy_views import *


class TokenBlacklistAPIView(generics.ListCreateAPIView):
    queryset = TokenBlacklist.objects.all()
    serializer_class = TokenBlacklistSerializer


class TokenBlacklistDetailView(generics.RetrieveUpdateAPIView):
    queryset = TokenBlacklist.objects.all()
    serializer_class = TokenBlacklistSerializer


class TokenBlacklistBulkAPIView(SyBulkView):
    queryset = TokenBlacklist.objects.all()
    serializer_class = TokenBlacklistSerializer
    model_class = TokenBlacklist


@csrf_exempt
def verify_jwt(request):
    authorization_header = request.headers.get("Authorization")

    if not authorization_header:
        return JsonResponse({"error": "Missing authorization header"}, status=401)

    token = authorization_header.split(" ")[1]

    try:
        decoded_token = jwt.decode(
            jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
        )
        username = decoded_token["user"]
        user = User.objects.get(username=username)
        expiration_time = datetime.datetime.fromtimestamp(decoded_token["exp"])

        if expiration_time - datetime.timedelta(days=1) <= datetime.datetime.now():
            exp = datetime.datetime.utcnow() + datetime.timedelta(days=7)
            payload = {"user": username, "exp": exp}
            refreshed_token = jwt.encode(
                payload,
                settings.SECRET_KEY,
                algorithm="HS256",
            )

            try:
                print("BLACKLISTED BLACKLISTED")
                old_token = TokenBlacklist.objects.get(token=token)
            except TokenBlacklist.DoesNotExist:
                old_token = TokenBlacklist(token=token)
                print("BLACKLISTED2 BLACKLISTED2")
                token = "None"

            old_token.save()

            return JsonResponse(
                {
                    "authenticated": True,
                    "is_superuser": user.is_superuser,
                    "username": username,
                    "refreshed_token": refreshed_token,
                    "exp": exp,
                },
                status=200,
            )

        if TokenBlacklist.objects.filter(token=token).exists():
            print("BLACKLISTED3 BLACKLISTED3")
            return JsonResponse({"authenticated": False}, status=401)

    except (jwt.exceptions.DecodeError, User.DoesNotExist, ObjectDoesNotExist):
        return JsonResponse({"authenticated": False}, status=401)

    return JsonResponse(
        {
            "authenticated": True,
            "is_superuser": user.is_superuser,
            "username": username,
        },
        status=200,
    )


@csrf_exempt
def get_salt_view(request):
    """Func String"""

    if request.method == "POST":
        data = json.loads(request.body)
        print(data)

        if not data["username"]:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        user = User.objects.get(username=data["username"])

        return JsonResponse({"salt": user.salt})

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def login_view(request):
    """Func String"""

    if request.method == "POST":
        data = json.loads(request.body)

        if not data["username"] or not data["password"]:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        user = authenticate(
            request, username=data["username"], password=data["password"]
        )

        if user is None:
            return JsonResponse({"error": "Invalid username or password"}, status=401)

        login(request, user)

        exp = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        payload = {"user": data["username"], "exp": exp}

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        response = JsonResponse(
            {
                "jwt": token,
                "authenticated": True,
                "is_superuser": user.is_superuser,
                "username": data["username"],
                "exp": exp,
            }
        )
        response.set_cookie(key="jwt", value=token, httponly=True, expires=exp)

        return response

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def register(request):
    """Func String"""

    if request.method == "POST":
        data = json.loads(request.body)
        print(data)

        if not data["username"] or not data["email"] or not data["password"]:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if len(data["password"]) < 6:
            return JsonResponse(
                {"error": "Password must be at least 6 characters"}, status=400
            )

        try:
            user = User.objects.create_user_with_settings(
                data["username"],
                data["email"],
                data["password"],
                data["firstName"],
                data["lastName"],
                data["phone"],
                data["address"],
                data["city"],
                data["state"],
                data["zipcode"],
                data["country"],
                data["salt"],
            )

        except IntegrityError:
            return JsonResponse(
                {"error": "Username or email already exists"}, status=400
            )

        return JsonResponse({"message": "User registered successfully"})

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def logout_view(request):
    authorization_header = request.headers.get("Authorization")

    if not authorization_header:
        return JsonResponse({"error": "Missing authorization header"}, status=401)

    token = authorization_header.split(" ")[1]

    try:
        decoded_token = jwt.decode(
            jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
        )
        username = decoded_token["user"]
        user = User.objects.get(username=username)
        logout(request)
        TokenBlacklist.objects.create(token=token)
        print("BLACKLISTED4 BLACKLISTED4")

        return JsonResponse({"message": "User logged out successfully"})

    except (jwt.exceptions.DecodeError, User.DoesNotExist):
        return JsonResponse({"error": "Error logging out the user"}, status=400)


@api_view(["PATCH", "GET"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.id)
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
