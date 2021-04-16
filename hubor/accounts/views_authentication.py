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
from data.models import NormalRange


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
        # Create accompany status and normal ranges of current patient
        if(user.user_type == 0):
            status = PatientStatus(patient = user, risk=0)
            temp_h = NormalRange(patient=user, vs="temp", type_of_range="h", value=37.2)
            temp_l = NormalRange(patient=user, vs="temp", type_of_range="l", value=34.0)
            hr_h = NormalRange(patient=user, vs="hr", type_of_range="h", value=130)
            hr_l = NormalRange(patient=user, vs="hr", type_of_range="l", value=60)
            rr_h = NormalRange(patient=user, vs="rr", type_of_range="h", value=60)
            rr_l = NormalRange(patient=user, vs="rr", type_of_range="l", value=16)
            spo2_h = NormalRange(patient=user, vs="spo2", type_of_range="h", value=100)
            spo2_l = NormalRange(patient=user, vs="spo2", type_of_range="l", value=90)
            bp_h = NormalRange(patient=user, vs="bp", type_of_range="h", value=130)
            bp_l = NormalRange(patient=user, vs="bp", type_of_range="l", value=60)
            unsaved = [user, status, temp_h, temp_l, hr_h, hr_l, rr_h, rr_l, spo2_h, spo2_l, bp_h, bp_l]
        else:
            unsaved = [user]
        saved = []
        try:
            counter = 0
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
            
            # save user and accompany status and normal ranges
            for item in unsaved:
                item.save()
                saved.append(item)

            return Response(response, status=200)
        except Exception as e:
            print(e)
            # if save failed, rollback
            for item in unsaved:
                item.delete()
            return Response(response, status=400)
    

    
# Logout View
class LogoutAPI(APIView):

    def post(self, request, *args, **kwargs):
        logout(request)
        response = {"query": "logout"}
        return Response(response, status=200)