from rest_framework import serializers

from user.models import CustomUser
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return obj.likes.values_list('id', flat=True)
    class Meta:
        model = Video
        fields = '__all__'
        extra_kwargs = {'likes': {'required': False}}


    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'is_verified', 'phone']

        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified': {'read_only': True},
        }