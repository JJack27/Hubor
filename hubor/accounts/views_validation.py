import json
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import *

# Check if given email address is already exist
class EmailValidation(APIView):
    
    # Receiving the email address and check if it's already exists
    def get(self, request, *args, **kwargs):
        # parsing the request
        email = kwargs['email']
        
        # retriving from database
        users = User.objects.filter(email=email)
        if len(users) == 0:
            return Response({}, status=200)
        else:
            return Response({}, status=409)


# Check if given username is already exist
class UsernameValidation(APIView):
    
    # Receiving the email address and check if it's already exists
    def get(self, request, *args, **kwargs):
        # parsing the request
        username = kwargs['username']
        
        # retriving from database
        users = User.objects.filter(username=username)
        if len(users) == 0:
            return Response({}, status=200)
        else:
            return Response({}, status=409)


# Check if given phone number is already exist
class PhoneValidation(APIView):
    
    # Receiving the email address and check if it's already exists
    def get(self, request, *args, **kwargs):
        # parsing the request
        phone = kwargs['phone']
        
        # retriving from database
        users = User.objects.filter(phone=phone)
        if len(users) == 0:
            return Response({}, status=200)
        else:
            return Response({}, status=409)