from django.urls import path, include
from rest_framework import routers
from .views import LoginView, SignupView, VideoView

router = routers.DefaultRouter()

urlpatternd = [
    
    path('login/',  LoginView.as_view(), name='login'),
    path("signup/", SignupView.as_view(), name='signup'),
    path('videos/<int:pk/', VideoView.as_view(), name='video_detail'),
    path("", include(router.urls))
]