from rest_framework import serializers
from .models import AuthorizedImg

class AuthorizedImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorizedImg
        fields = ['authorized_img','person_name','uploaded_datetime','user_id']