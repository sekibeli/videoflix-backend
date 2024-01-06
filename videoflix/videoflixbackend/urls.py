from django.urls import path, include
from rest_framework import routers
from .views import LoginView, SignupView, VideoViewSet

router = routers.DefaultRouter()

router.register(r'videos', VideoViewSet, basename='video')

urlpatterns = [
    
    path('login/',  LoginView.as_view(), name='login'),
    path("signup/", SignupView.as_view(), name='signup'),
    path("", include(router.urls))
]