from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ROMO
from .serializers import RomoRegisterSerializer
from django.contrib.auth.models import User
import datetime, jwt
import paho.mqtt.client as mqtt

@api_view(['POST'])
def register_romo(request):
    response = Response()

    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        # print(user.is_authenticated)

        if user.is_authenticated:
            new_romo_info = request.data
            data = {
                "mac_address" : new_romo_info['mac_address'],
                "romo_label" : new_romo_info['romo_label'],
                "status" : new_romo_info['status'],
                "last_active" : datetime.datetime.now(),
                "user_id" : user.id,
            }
            # print("above?")

            serializer = RomoRegisterSerializer(data=data)
            if serializer.is_valid():
                print("valid?")
                serializer.save()
                response.data = data
                response.status_code = 200    
            else:
                ## Because the mac address is unique, so data won't be abled to save
                response.data={
                    'message' : "Mac address alreay exists!"
                }
                response.status_code = 400  
                    

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

@api_view(['GET'])
def get_romo_data(request):
    response = Response()

    ## If the user only has one romo device
    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        # print(user.is_authenticated)

        if user.is_authenticated:
            # romo_data_array = ROMO.objects.filter(user_id=user.id)
            romo_data = ROMO.objects.all().filter(user_id=user.id).get()
            response.data = {
                'romo_info' : {
                    'id' : romo_data.id,
                    'romo_label' : romo_data.romo_label,
                    'mac_address' : romo_data.mac_address,
                    'status' : romo_data.status,
                    'last_active' : romo_data.last_active,
                    'user_id' : romo_data.user_id.id,
                }
            }

            print(response.data["romo_info"]["last_active"])

            response.status_code = 200
        
    ## If the user has multiple romo devices
    except ROMO.MultipleObjectsReturned:
        romo_data_array = []
        romo_data = ROMO.objects.all().filter(user_id=user.id)            
        
        for x in romo_data:
            romo_data_array.append({
                'id' : x.id,
                'romo_label' : x.romo_label,
                'mac_address' : x.mac_address,
                'status' : x.status,
                'last_active' : x.last_active,
                'user_id' : x.user_id.id,
            })

        response.data = {
            'romo_info' : romo_data_array
        }
        response.status_code = 200
        
    ## If the user do not has any romo devices
    except ROMO.DoesNotExist:
        response.status_code = 404

    ## If the user's token expired     
    except jwt.ExpiredSignatureError:
        response.data = {
            "message": "Unauthenticated!",
        }

        response.status_code = 401

    ## If the user's token not found and unauthorized
    except jwt.exceptions.DecodeError:
        response.data = {
            "message": "Not token found!",
        }

        response.status_code = 404

    return response    

@api_view(['DELETE'])
def delete_romo(request, mac_address):
    response = Response()

    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()

        if user.is_authenticated:
            romo_data = ROMO.objects.all().filter(user_id=user.id).all().filter(mac_address=mac_address)

            if len(romo_data) >= 1:
                romo_data.delete()
                response.status_code = 204
            else:
                response.status_code = 404


        ## If the user's token expired     
    except jwt.ExpiredSignatureError:
        response.data = {
            "message": "Unauthenticated!",
        }

        response.status_code = 401

    ## If the user's token not found and unauthorized
    except jwt.exceptions.DecodeError:
        response.data = {
            "message": "Not token found!",
        }

        response.status_code = 404

    return response    

@api_view(['PUT'])
def update_romo(request):
    response = Response()

    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()
        # print(user.is_authenticated)

        if user.is_authenticated:
            romo_data = ROMO.objects.get(user_id=user.id, mac_address=request.data['mac_address'])
            # print(request.data['last_active'])
            new_romo_info = request.data
            data = {
                "mac_address" : new_romo_info['mac_address'],
                "romo_label" : new_romo_info['romo_label'],
                "status" : new_romo_info['status'],
                "last_active" : datetime.datetime.fromtimestamp(int(new_romo_info['last_active'])),
                "user_id" : user.id,
            }

            serializer = RomoRegisterSerializer(romo_data, data=data)
            if serializer.is_valid():
                # update existing data
                serializer.save()
                response.data = data
                response.status_code = 200    
            else:
                ## Because the mac address is unique, so data won't be abled to save
                response.data={
                    'message' : "Mac address alreay exists!"
                }
                response.status_code = 400  

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

@api_view(['GET'])
def get_romo_user_data(request, mac_address):  
    response = Response() 

    try :
        user_data = ROMO.objects.get(mac_address=mac_address)

        # get user object
        user = user_data.user_id

        response.data = {"username": user.username}
        response.status_code = 200

    except ROMO.DoesNotExist:
        response.data = {"username": "Not Found"}
        response.status_code = 404

    return response