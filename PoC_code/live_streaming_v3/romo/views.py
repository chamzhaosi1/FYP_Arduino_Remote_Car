from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ROMO
from .serializers import RomoRegisterSerializer
from datetime import datetime  

@api_view(['POST'])
def register_romo(request):
    user = request.user
    
    if user.is_authenticated:
        new_romo_info = request.data

        data = {
            "mac_address" : new_romo_info['mac_address'],
            "romo_label" : new_romo_info['romo_label'],
            "status" : new_romo_info['status'],
            "last_active" : datetime.now(),
            "user_id" : user.id,
        }

        serializer = RomoRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response({'error': 'Something wrong happen!'})

@api_view(['GET'])
def get_romo_data(request):
    user = request.user
    
    if user.is_authenticated:
        try:
            # romo_data_array = ROMO.objects.filter(user_id=user.id)
            romo_data = ROMO.objects.all().filter(user_id=user.id).get()
            return Response({
                'romo_info' : {
                    'id' : romo_data.id,
                    'romo_label' : romo_data.romo_label,
                    'status' : romo_data.status,
                    'last_active' : romo_data.last_active,
                    'user_id' : romo_data.user_id.id,
                }
            })
            # return Response(status=status.HTTP_404_NOT_FOUND)
        except ROMO.MultipleObjectsReturned:
            romo_data_array = []
            romo_data = ROMO.objects.all().filter(user_id=user.id)            
            
            for x in romo_data:
                romo_data_array.append({
                    'id' : x.id,
                    'romo_label' : x.romo_label,
                    'status' : x.status,
                    'last_active' : x.last_active,
                    'user_id' : x.user_id.id,
                })

            return Response({
                'romo_info' : romo_data_array
            })
        
        except ROMO.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        