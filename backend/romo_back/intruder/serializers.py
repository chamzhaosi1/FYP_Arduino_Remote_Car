from rest_framework import serializers
from .models import IntruderImg

class IntrusionImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntruderImg
        fields = ['intruder_img', 'intruder_label_id', 'romo_id', 'uploaded_datetime', 'user_id']
