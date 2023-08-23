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
    response = Response()
<<<<<<< HEAD

    # serializer.is_valid(raise_exception=True)
    if serializer.is_valid():
        user = serializer.validated_data['user']

        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret1188', algorithm='HS256')

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message' : "login successfully",
            'username' : user.username,
            'status_code' : "200"
        }

    else:
        # print("Invalid username or password")

        response.data = {
            'message' : "Invalid username or password, please try again!",
            'status_code' : "404"
        }

    return response

=======
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]

    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, "secret1188", algorithm="HS256")

    response.set_cookie(key="jwt", value=token, httponly=True)
    response.data = {
        "message": "login successfully",
        "username": user.username,
    }

    response.status_code = 200

    return response

>>>>>>> 4e52e1bf6d27bcc70a1b614bdcfd759fc4e467b0

@api_view(["GET"])
def get_user_data(request):
    response = Response()
<<<<<<< HEAD
    
    try:
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret1188', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        # print(user.is_authenticated)

        if user.is_authenticated:
            return Response({
                'user_info':{
                    'id' : user.id,
                    'username' : user.username,
                    'email': user.email
                },
            })
=======

    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        # print(user.is_authenticated)

        if user.is_authenticated:
            return Response(
                {
                    "user_info": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )
>>>>>>> 4e52e1bf6d27bcc70a1b614bdcfd759fc4e467b0

    except jwt.ExpiredSignatureError:
        # raise AuthenticationFailed('Unauthenticated!')
        response.data = {
<<<<<<< HEAD
            'message' : "Unauthenticated!",
            'status_code' : "401"
        }

    except jwt.exceptions.DecodeError:
        response.data = {
            'message' : "Not token found!",
            'status_code' : "401"
        }

=======
            "message": "Unauthenticated!",
        }

        response.status_code = 401

    except jwt.exceptions.DecodeError:
        response.data = {
            "message": "Not token found!",
        }

        response.status_code = 404

>>>>>>> 4e52e1bf6d27bcc70a1b614bdcfd759fc4e467b0
    return response


@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    _, token = AuthToken.objects.create(user)

    return Response(
        {
            "user_info": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "token": token,
        }
    )
