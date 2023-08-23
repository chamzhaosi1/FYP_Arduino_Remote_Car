from django.http import JsonResponse
# from .models import User
# from .serializers import UserSerializer
from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# @api_view(['GET', 'POST'])
# def users_list(request, format=None):
#   if request.method == 'GET':
#     #get all the drinks
#     users = User.objects.all()
    
#     #serialize them
#     serializer = UserSerializer(users, many=True)

#     #return json
#     # return JsonResponse(serializer.data, safe=False) # if we want to return non-dict object (date type) we need to set safe = False
#     return JsonResponse({"drinks":serializer.data}) # However, if it is dict object
  
#   if request.method == 'POST':
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def user_detail(request, format=None):
#   if request.method == 'POST':
#     username = request.POST["username"]
#     password = request.POST["password"]
#     user = User.objects.filter(username=username, password=password)
#     print(user)

#     if user is not None:
#       return JsonResponse({"message":"login success"})
