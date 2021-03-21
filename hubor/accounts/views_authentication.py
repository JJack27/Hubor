from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import uuid
import re
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
import datetime
import dateutil
import pytz
from accounts.models import *
from accounts.serializers import *
from .views_utils import *


'''
================ Authentication ==============
'''
# Login API
# /api/login/
# response {
#   query: login
#   id: uuid
# }
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        session = request.session 
        request_body = request.data
        user = request.user
        user_cache = authenticate(request, username=request_body['username'], password=request_body['password'])
        try:
            login(request, user_cache, backend='django.contrib.auth.backends.ModelBackend')
        except:
            return Response({}, status=403)
        else:
            if user_cache == None:
                return Response({}, status=403)
            query = User.objects.get(id = user_cache.id)
            response = BaseUserSerializer(query).data
            return Response(response, status=200)

# Register API
# /api/register/
class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        request_body = request.data
        response = {"query": "registration"}
        
        # validate date of birth
        date_of_birth = dateutil.parser.parse(request_body['date_of_birth'])
          
        if date_of_birth > datetime.datetime.now(tz=pytz.timezone("UTC")):
            return Response(response, status=400)
        
        date_of_birth = date_of_birth.strftime("%Y-%m-%d")
        # parse request
        user = User(
            username = request_body['username'],
            email = request_body['email'],
            height = float(request_body['height']),
            weight = float(request_body['weight']),
            user_type = int(request_body['user_type']),
            phone = request_body['phone'],
            date_of_birth = date_of_birth,
            gender = int(request_body['gender']),
            notes = request_body['notes'],
            first_name = request_body['first_name'],
            last_name = request_body['last_name']
            )
        
        user.set_password(request_body['password'])
        
        try:
            user.save()
            response['data'] = {
                'id': user.id,
                'email': user.email,
                'weight': user.weight,
                'height': user.height,
                'user_type': user.user_type,
                'phone': user.phone,
                'date_of_birth': user.date_of_birth,
                'gender': user.gender,
                'notes': user.notes,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            # Create accompany status of current patient
            if(user.user_type == 0):
                status = PatientStatus(patient = user, risk=0)
                status.save()
            return Response(response, status=200)
        except Exception as e:
            print(e)
            return Response(response, status=400)
    

    
# Logout View
class LogoutAPI(APIView):

    def post(self, request, *args, **kwargs):
        logout(request)
        response = {"query": "logout"}
        return Response(response, status=200)