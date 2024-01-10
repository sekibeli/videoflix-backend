"""
URL configuration for videoflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from videoflixbackend.views import (
    LoginView, 
    SignupView, 
    LogoutView, 
    VerifyEmailView,
    LoggeduserView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('videoflixbackend.urls')),
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit-user/', LoggeduserView.as_view(), name='user-info'),

    path('__debug__/', include('debug_toolbar.urls')),
    path('django_rq/', include('django_rq.urls')),  


]  + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
