from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework import status
from rest_framework import viewsets
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .serializers import VideoSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Video
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.
class LoginView(APIView):
    # @cache_page(CACHE_TTL)
    def post(self, request, *args, **kwargs):
        email = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
       
        if user:
            print('Hi')
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            return Response({
                'token': token.key,
                'user_id': user.pk
                
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=http_status.HTTP_400_BAD_REQUEST)
 
class SignupView(APIView):
    
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('username')
        password = request.data.get('password')

        if not all([first_name, last_name, email, password]):
            return Response({'error': 'Alle Felder müssen ausgefüllt sein.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=email).exists():
            return Response({'error': 'Dieser Benutzer existiert bereits.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)       
        


class VideoView(viewsets.ModelViewSet):
    
    serializer_class = VideoSerializer
    # permission_classes = [IsAuthenticated]
 
    # @cache_page(CACHE_TTL)
    def get_queryset(self):
        # current_user = self.request.user #eingloggten user holen
        # if current_user.is_authenticated:
       
            return Video.objects.all()
            # return Video.objects.filter(category=category)
        # return Video.objects.none()
    

         
class VideoDetailView(APIView):
    
    # @cache_page(CACHE_TTL)
    def get(self,request,pk, format=None):
        try:
            video = Video.objects.get(pk=pk)
            serializer = VideoSerializer(video)
            return Response(serializer.data)
        except Video.DoesNotExist:
            return Response({'error': 'Video existiert nicht'}, status=status.HTTP_404_NOT_FOUND)