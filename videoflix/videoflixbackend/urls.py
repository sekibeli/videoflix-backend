from django.urls import path, include
from rest_framework import routers

from user.views import LoginView, SignupView
from .views import VideoViewSet

router = routers.DefaultRouter()

router.register(r'videos', VideoViewSet, basename='video')


urlpatterns = [
    
    path('login/',  LoginView.as_view(), name='login'),
    path("signup/", SignupView.as_view(), name='signup'),
    path("", include(router.urls))
]