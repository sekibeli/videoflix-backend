from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status as http_status

# Create your views here.
class LoginView(APIView):
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
       
        if user:
            print('Hi Schnecki')
            # token, created = Token.objects.get_or_create(user=user)
            # print(token)
            # return Response({
            #     'token': token.key,
            #     'user_id': user.pk
                
            # })
        else:
            return Response({'detail': 'Invalid credentials'}, status=http_status.HTTP_400_BAD_REQUEST)