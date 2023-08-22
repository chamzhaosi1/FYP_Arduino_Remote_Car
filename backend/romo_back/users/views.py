from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
import datetime, jwt

# Create your views here.
@api_view(["POST"])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data["user"]

    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, "secret1188", algorithm="HS256")

    response = Response()
    response.set_cookie(key="jwt", value=token, httponly=True)
    response.data = {
        "message": "login successfully",
    }
    response.status_code = 200
    return response


@api_view(["GET"])
def get_user_data(request):
    response = Response()

    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        # print(user.is_authenticated)

        if user.is_authenticated:
            return Response(
                {
                    "user_info": {
                        # "id": user.id,
                        "username": user.username,
                        "first_name" : user.first_name,
                        "last_name" : user.last_name,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )

    except jwt.ExpiredSignatureError:
        # raise AuthenticationFailed('Unauthenticated!')
        response.data = {
            "message": "Unauthenticated!",
        }

        response.status_code = 401

    except jwt.exceptions.DecodeError:
        response.data = {
            "message": "Not token found!",
        }

        response.status_code = 404

    return response


@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, "secret1188", algorithm="HS256")

    response = Response()
    response.set_cookie(key="jwt", value=token, httponly=True)
    response.data = {
        "message": "register successfully",
        "username": user.username,
    }
    response.status_code = 200
    return response


@api_view(["POST"])
def logout(request):
    response = Response()
    # response.set_cookie(key="jwt", value="token", httponly=True)
    response.delete_cookie('jwt')
    response.data = {
        'message' : 'success'
    }
    # response.status_code = 200
    return response