from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect
import os
from django.http import HttpResponse
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://127.0.0.1:8000/home'
success_string1 = 'yay'
request_token_url = 'https://channeli.in/open_auth/token/'
request_data_url = 'https://channeli.in/open_auth/get_user_data/'


params = {'client_id': client_id,
        'client_secret': client_secret, 
        'grant_type': 'authorization_code',
        'code': '' ,
        'redirect_uri' : redirect_uri,
        'state': success_string1}

class RequestAccessAPI(APIView):
    def get(self, request):
        print(client_id)
        URL= 'https://channeli.in/oauth/authorise' + "?client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&state=" + success_string1
        return redirect(URL)

class HelloWorldView(APIView):
    def get(self, request):
        return HttpResponse("Hello, World!")

class SignUpView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
