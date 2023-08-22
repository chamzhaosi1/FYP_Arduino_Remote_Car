from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from romos.models import ROMO
from .models import IntruderImg
import datetime, jwt, base64, os

from .serializers import IntrusionImgSerializer
from authorized.serializers import AuthorizedImgSerializer
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

@api_view(['POST'])
def intr_img_upload(request):
    response = Response()
    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()

        new_uploaded_img = request.data
        romo = ROMO.objects.filter(mac_address=new_uploaded_img["mac_address"]).first()

        print("New uploaded image info: ", new_uploaded_img)

        data = {
            "intruder_img" : new_uploaded_img['intruder_img'],
            "intruder_label_id" : new_uploaded_img['intruder_label_id'],
            "romo_id" : romo.id,
            "uploaded_datetime": datetime.datetime.now(),
            "user_id" : user.id,
        }

        print(data)

        serializer = IntrusionImgSerializer(data=data)
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
def get_intr_img(request):  
    response = Response()
    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()

        uploadedImg = IntruderImg.objects.all().filter(user_id=user.id)
        # print(len(uploadedImg))

        # Whether it is multuple result or only one result, return array to frontend
        if len(uploadedImg) == 1:
            # convert the image to base64 encode to using json format send to frontend
            encoded_data = base64.b64encode(uploadedImg[0].intruder_img.read()).decode('utf-8')
            data_url = 'data:image/jpeg;base64,' + encoded_data
            data = {
                'image_info' : [{'image': data_url, 
                                 "name":uploadedImg[0].intruder_label_id, 
                                 "mac_address": uploadedImg[0].romo_id.mac_address,
                                 "date_time":uploadedImg[0].uploaded_datetime, 
                                 "id": uploadedImg[0].id}]
            }

        else :
            image_array = []
            for obj in uploadedImg:
                encoded_data = base64.b64encode(obj.intruder_img.read()).decode('utf-8')
                data_url = 'data:image/png;base64,' + encoded_data

                image_array.append({
                    "image": data_url, 
                    "mac_address": obj.romo_id.mac_address,
                    "name":obj.intruder_label_id, 
                    "date_time":obj.uploaded_datetime,
                    "id": obj.id
                })

            data = {
                'image_info': image_array
            }

        response.data = data
        response.status_code = 200

    except IntruderImg.DoesNotExist:
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

@api_view(['PUT'])
def upt_intr_img(request):
    response = Response()

    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()

        if user.is_authenticated:
            new_uploaded_img = request.data
            print(new_uploaded_img)
            obj = IntruderImg.objects.filter(intruder_label_id=new_uploaded_img['intruder_label_id']).first()
            obj.intruder_img = new_uploaded_img['intruder_img']
            obj.uploaded_datetime = datetime.datetime.now()

            obj.save()
            response.status_code = 200

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
def covert_intr_to_auth(request):
    response = Response()
    
    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()

        if user.is_authenticated:
            convert_img_info = request.data
            print(convert_img_info)

            # Intruder image folder path
            intr_folder_path = os.path.join("media/intrusion", user.username, convert_img_info["intruder_img_label"])

            # Get all imges from the path 
            # Loop all the image in the folder
            for imgs in os.listdir(intr_folder_path):
                image_path = os.path.join(intr_folder_path, imgs)
                #  read the image byte
                with open(image_path, 'rb') as file:
                    image_data = file.read()

                data = {
                    "authorized_img" : convert_byte_image(image_data),
                    "person_name": convert_img_info['person_name'].lower().replace(" ", "_"),
                    "uploaded_datetime": datetime.datetime.now(),
                    "user_id" : user.id,
                }

                print(data)
                
                serializer = AuthorizedImgSerializer(data=data)
                serializer.is_valid(raise_exception=True)

                if serializer.is_valid():
                    serializer.save()
                    response.status_code = 201

                else:
                    response.status_code = 400


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


def convert_byte_image(byte_image):
    # Create a ContentFile from the byte image
    content_file = ContentFile(byte_image)

    # Create an InMemoryUploadedFile object
    uploaded_file = InMemoryUploadedFile(
        content_file,
        field_name=None,  # The name of the form field
        name='convert.jpg',  # The desired name for the file
        content_type='image/jpeg',  # The content type of the file
        size=len(byte_image),  # The size of the file in bytes
        charset='utf-8'  # The character encoding of the file
    )

    return uploaded_file


@api_view(['DELETE'])
def del_intr_img(request, id):  
    response = Response()

    try:
        token = request.COOKIES.get("jwt")
        payload = jwt.decode(token, "secret1188", algorithms=["HS256"])
        user = User.objects.filter(id=payload["id"]).first()

        if user.is_authenticated:
            auth_img_data = IntruderImg.objects.all().filter(user_id=user.id).all().filter(id=id)

            if len(auth_img_data) >= 1:
                
                # to delete all of the image inside the intruder folder
                intruder_label = auth_img_data[0].intruder_label_id
                intruder_folder_path = os.path.join("media/intrusion", user.username, intruder_label)

                for pit in os.listdir(intruder_folder_path):
                    print(os.path.join(intruder_folder_path, pit))
                    os.remove(os.path.join(intruder_folder_path, pit))
                    # os.path.join(intruder_folder_path, pit).delete()

                # delete the image file from the file system
                # auth_img_data[0].intruder_img.delete()

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