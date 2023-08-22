from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import AuthorizedImg
import datetime, jwt
import base64

from .serializers import AuthorizedImgSerializer

@api_view(['POST'])
def auth_img_upload(request):
    response = Response()
    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()

        new_uploaded_img = request.data
        print("New uploaded image info: ", new_uploaded_img)
        # print("sdfsdfsdf")
        # print(new_uploaded_img)
        data = {
            "authorized_img" : new_uploaded_img['authorized_img'],
            "person_name": new_uploaded_img['person_name'],
            "uploaded_datetime": datetime.datetime.now(),
            "user_id" : user.id,
        }

        print(data)

        serializer = AuthorizedImgSerializer(data=data)
        # serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            serializer.save()
            response.status_code = 201
        else:
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
def get_auth_img(request):  
    response = Response()
    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()

        uploadedImg = AuthorizedImg.objects.all().filter(user_id=user.id)
        # print(len(uploadedImg))

        # Whether it is multuple result or only one result, return array to frontend
        if len(uploadedImg) == 1:
            # convert the image to base64 encode to using json format send to frontend
            encoded_data = base64.b64encode(uploadedImg[0].authorized_img.read()).decode('utf-8')
            data_url = 'data:image/png;base64,' + encoded_data
            data = {
                'image_info' : [{'image': data_url, "name":uploadedImg[0].person_name, "id": uploadedImg[0].id}]
            }

        else :
            image_array = []
            for obj in uploadedImg:
                encoded_data = base64.b64encode(obj.authorized_img.read()).decode('utf-8')
                data_url = 'data:image/png;base64,' + encoded_data

                image_array.append({
                'image': data_url, "name":obj.person_name, "id": obj.id
                })

            data = {
                'image_info': image_array
            }

        response.data = data
        response.status_code = 200

    except AuthorizedImg.DoesNotExist:
        response.status_code = 404

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

@api_view(['DELETE'])
def del_auth_img(request, id):  
    response = Response()

    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()

        if user.is_authenticated:
            auth_img_data = AuthorizedImg.objects.all().filter(user_id=user.id).all().filter(id=id)

            if len(auth_img_data) >= 1:
                # delete the image file from the file system
                auth_img_data[0].authorized_img.delete()

                # delete the model instance from the database
                auth_img_data.delete()

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