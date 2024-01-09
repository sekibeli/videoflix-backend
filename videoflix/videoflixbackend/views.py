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
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from django.utils.decorators import method_decorator

from rest_framework.parsers import MultiPartParser, FormParser

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class SignupView(APIView):    
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if CustomUser.objects.filter(email=request.data["email"]).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

            user = CustomUser(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                phone=serializer.validated_data.get('phone', ''),
                # address=serializer.validated_data.get('address', ''),
            )
            user.set_password(serializer.validated_data['password'])  
            user.save()

            self.send_verification_email(user)

            return Response({"user": CustomUserSerializer(user).data}, status=status.HTTP_201_CREATED)


    

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


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)     


class VideoViewSet(viewsets.ModelViewSet):
    
    serializer_class = VideoSerializer
    # permission_classes = [IsAuthenticated]
   
   
    # @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super(VideoViewSet, self).list(request, *args, **kwargs)
 
  #  @cache_page(CACHE_TTL)
    def get_queryset(self):
        # current_user = self.request.user #eingloggten user holen
        # if current_user.is_authenticated:
        queryset = Video.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset          
 