from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import VideoSerializer
from .models import Video

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class VideoViewSet(viewsets.ModelViewSet):
    
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
   
   
    # @method_decorator(cache_page(CACHE_TTL))
    # def list(self, request, *args, **kwargs):
    #     return super(VideoViewSet, self).list(request, *args, **kwargs)
 
    def list(self, request, *args, **kwargs):
        cache_key = 'video_list_cache_key'
        video_list = cache.get(cache_key)

        if not video_list:
            response = super(VideoViewSet, self).list(request, *args, **kwargs)
            video_list = response.data
            cache.set(cache_key, video_list, timeout=CACHE_TTL)

        return Response(video_list)
    
    
  #  @cache_page(CACHE_TTL)
    def get_queryset(self):
        current_user = self.request.user #eingloggten user holen
        if current_user.is_authenticated:
            queryset = Video.objects.all()
                    
            category = self.request.query_params.get('category', None)
            if category is not None:
                    queryset = queryset.filter(category=category)
        return queryset      
    
   
    def perform_create(self, serializer):
        serializer.save(created_from=self.request.user)
 



        
