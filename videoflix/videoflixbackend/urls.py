from django.urls import path, include
from rest_framework import routers
from .views import LoginView

router = routers.DefaultRouter()

urlpatternd = [
    
    path('login/',  LoginView.as_view(), name='login'),
    path("", include(router.urls))
]