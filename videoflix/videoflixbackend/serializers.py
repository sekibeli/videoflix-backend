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
        fields = ['id', 'username', 'email', 'password', 'is_verified', 'phone']

        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified': {'read_only': True},
        }

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        password = validated_data.get('password')
        if password:
            user.set_password(password)
        user.save()
        return user