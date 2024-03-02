from rest_framework import serializers
from django.conf import settings
from user.models import CustomUser
from .models import Video, VideoQuality

class VideoSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField('get_video_url')

    class Meta:
        model = Video
        fields = '__all__'  
        extra_kwargs = {'likes': {'required': False}}

    def get_video_url(self, obj):
        request = self.context.get('request')
        video_url = obj.video_file.url if obj.video_file else ''
        if request is not None:
            return request.build_absolute_uri(video_url)
        return video_url 
    

class VideoQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoQuality
        fields = ('quality', 'video_file')

    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'is_verified', 'phone']

        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified': {'read_only': True},
        }