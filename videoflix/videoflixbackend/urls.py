from django.urls import path, include
from rest_framework import routers
from .views import LoginView, SignupView, VideoView, VideoDetailView

router = routers.DefaultRouter()
router.register(r'videos', VideoView, basename='video')

urlpatterns = [
    
    path('login/',  LoginView.as_view(), name='login'),
    path("signup/", SignupView.as_view(), name='signup'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path("", include(router.urls))
]