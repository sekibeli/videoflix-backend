from rest_framework import serializers

from user.models import CustomUser
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'is_verified', 'phone', 'adress']

        extra_kwargs = {
            'is_verified': {'read_only': True},
        }