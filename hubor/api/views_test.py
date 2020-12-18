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
# /api/test/
class TestView(APIView):

    def post(self, request, *args, **kwargs):
        request_body = request.data
        print(request_body)
        return Response({"query":'test'}, status=200)

    
class AllAPIView(APIView):

    def get(self, request, *args, **kwargs):
        available_urls = [
            'emailvalidation/', 
            'usernamevalidation/', 
            'register/',
            'login/',
            'logout/', 
            'bracelet/<uuid:owner>/',
            'takecareof/<uuid:doctor>/<uuid:patient>/', 
            'patientsof/<uuid:doctor>/', 
            'doctorof/<uuid:patient>/', 
            'doctors/',
            'shortdoctors/',
            'facilities/', 
            'belongsto/<uuid:facility>/',


            # Data related
            'data/<uuid:pk>/', 
            'vs/<uuid:owner>/', 

            # Emergency related
            'emergency/<uuid:pk>/', 
            'emergencycontact/<uuid:pk>/', 

            # Configuration
            'latestconfig/', 

            # test
            'test/', 
        ]
        return Response(data=available_urls, status=200)
