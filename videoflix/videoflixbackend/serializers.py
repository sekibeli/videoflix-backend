from rest_framework import serializers
from django.conf import settings
from user.models import CustomUser
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField('get_video_url')

    class Meta:
        model = Video
        fields = '__all__'  
        extra_kwargs = {'likes': {'required': False}}

    def get_video_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.video_file.url) 
        return obj.file.url  

    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'is_verified']

        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified': {'read_only': True},
        }