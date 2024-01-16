from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import VideoSerializer
from .models import Video

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class VideoViewSet(viewsets.ModelViewSet):
    
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
   
   
    # @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super(VideoViewSet, self).list(request, *args, **kwargs)
 
  #  @cache_page(CACHE_TTL)
    def get_queryset(self):
        current_user = self.request.user #eingloggten user holen
        if current_user.is_authenticated:
            queryset = Video.objects.all()
            category = self.request.query_params.get('category', None)
            if category is not None:
                    queryset = queryset.filter(category=category)
        return queryset      
    
   
    
 
# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = CustomUserSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         if self.request.user.is_authenticated:
#             return CustomUser.objects.all()  
#         return CustomUser.objects.none() 



        