from django.shortcuts import render
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
from accounts.models import *
from accounts.serializers import *
# Create your views here.


# Register API
# /api/register/
class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        request_body = request.data
        response = {"query": "registration"}
        
        # validate date of birth
        date_of_birth = datetime.datetime.strptime(request_body['date_of_birth'], '%Y-%m-%d')
        if date_of_birth > datetime.datetime.now():
            return Response(response, status=401)
        
        # parse request
        user = User(
            username = request_body['username'],
            email = request_body['email'],
            height = request_body['height'],
            weight = request_body['weight'],
            user_type = request_body['user_type'],
            phone = request_body['phone'],
            date_of_birth = request_body['date_of_birth'],
            gender = request_body['gender'],
            notes = request_body['notes']
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
                'notes': user.notes
            }
            return Response(response, status=200)
        except Exception as e:
            print(e)
            return Response(response, status=401)
    
# Login API
# /api/login/
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        session = request.session 
        request_body = request.data
        response = {'query': 'login'}
        user = request.user
        user_cache = authenticate(request, username=request_body['username'], password=request_body['password'])
        
        try:
            login(request, user_cache, backend='django.contrib.auth.backends.ModelBackend')
        except:
            return Response(response, status=403)
        else:
            if user_cache == None:
                return Response(response, status=403)
            response = {"id": user_cache.id}
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

'''
/api/bracelet/<uuid:owner>/
APIs for adding and retrieving bracelets
'''
class BraceletAPI(APIView):
    model = Bracelet
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)
    
    '''
    POST
    - Accepting adding bracelet for given user-uuid
    - payload:
        {
            mac_addr: String
        }
    '''
    def post(self, request, *args, **kwargs):
        owner = kwargs['owner']
        request_body = request.data
        request_body['owner'] = owner
        response = {'query':'bracelet'}

        # validate mac_addr
        try True:
            valid = re.search('^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$', request_body['mac_addr'])
            if valid:
                serializer = BraceletSerializer(data = request_body)
                if(serializer.is_valid()):
                    bracelet = serializer.save()
                    response['bracelet'] = BraceletSerializer(bracelet).data
                    return Response(response, status=200)
                
            return Response(response, status=401)
        except Exception as e:
            print(e)
            return Response(response, status=401)
    
    '''
    GET
    - get all bracelets of given owner
    - return:
        {
            query: bracelet
            bracelets: [
                {bracelet_1},
                {bracelet_2},
                ...
            ]
        }
    '''
    def get(self, request, *args, **kwargs):
        response = {"query":"bracelet"}

        # get bracelets from given user
        owner = kwargs['owner']
        query = Bracelet.objects.filter(owner=owner)
        bracelets = BraceletSerializer(query, many=True).data
        response['bracelets'] = bracelets

        # Check if the user has no bracelets
        if bracelets == []:
            return Response(response, status=404)
        else:
            return Response(response, status=200)
                