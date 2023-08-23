from rest_framework import serializers
from .models import ROMO

class RomoRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ROMO
        fields = ['mac_address', 'romo_label', 'status', 'last_active', 'user_id']