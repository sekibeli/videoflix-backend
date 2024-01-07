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
from user.models import CustomUser
from .serializers import VideoSerializer, CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Video
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class SignupView(APIView):    
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if CustomUser.objects.filter(email=request.data["email"]).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.is_valid(raise_exception=True)        
        user = serializer.save()

        self.send_verification_email(user)

        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
    

    def send_verification_email(self, user):
        subject = 'Please confirm your email'
        message = f'Please use this link to verify your email: {settings.FRONTEND_URL}/verify/{user.verification_token}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


class VerifyEmailView(APIView):
    def get(self, request, token, format=None):
        try:
            user = CustomUser.objects.get(verification_token=token)
            user.is_verified = True
            user.save()
            return Response({"message": "E-Mail successfully verified."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invaild Token"}, status=status.HTTP_400_BAD_REQUEST)
        
 
class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if not user.is_verified:
                return Response({"error": "Please verify your email first."}, status=status.HTTP_401_UNAUTHORIZED)

            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid login data"}, status=status.HTTP_401_UNAUTHORIZED)             


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