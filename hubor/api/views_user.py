from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import uuid
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail

from accounts.models import User
# Create your views here.


# Register API
# /api/register/
class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        request_body = request.data['values']
        response = {"query": "registration"}
        user = User(
            username = request_body['username'],
            email = request_body['email'],
            height = request_body['height'],
            weight = request_body['weight'],
            user_type = request_body['user_type']
            )
        user.set_password(request_body['password'])
        try:
            user.save()
            response['success'] = 'true'
            return Response(response, status=200)
        except:
            response['success'] = 'false'
            return Response(response, status=500)
    
# Login API
# /api/login/
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        session = request.session 
        request_body = request.data["values"]
        user = request.user 
        print(request_body)
        user_cache = authenticate(request, username=request_body['username'], password=request_body['password'])
        
        try:
            login(request, user_cache, backend='django.contrib.auth.backends.ModelBackend')
        except:
            response = {"success": "false", "id": 'None'}
            return Response(response, status=200)
        else:
            if user_cache == None:
                response = {"success": "false", "id": 'None'}
                return Response(response, status=200)
            response = {"success": "true", "id": user_cache.id}
            print(user_cache.id)
            return Response(response, status=200)
    
# Logout View
class LogoutAPI(APIView):

    def post(self, request, *args, **kwargs):
        print("User is logging out")
        logout(request)
        response = {"query": "logout"}
        return Response(response, status=200)


# Check if given email address is already exist
class EmailValidation(APIView):
    
    # Receiving the email address and check if it's already exists
    def post(self, request, *args, **kwargs):
        # parsing the request
        request_body = request.data
        response = {"query":'emailvalidation'}
        email_address = request_body['email']
        print(email_address)
        
        # retriving from database
        users = User.objects.filter(email=email_address)
        if len(users) == 0:
            response["valid"] = "true"
        else:
            response["valid"] = "false"
        
        return Response(response, status=200)

# Check if given username is already exist
class UsernameValidation(APIView):
    
    # Receiving the email address and check if it's already exists
    def post(self, request, *args, **kwargs):
        # parsing the request
        request_body = request.data
        response = {"query":'usernamevalidation'}
        username = request_body['username']
        
        # retriving from database
        users = User.objects.filter(username=username)
        if len(users) == 0:
            response["valid"] = "true"
        else:
            response["valid"] = "false"
        
        return Response(response, status=200)