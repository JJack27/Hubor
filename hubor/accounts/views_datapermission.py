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
/api/takecareof/<UUID:doctor>/<UUID:patient>/
API Represents the take-care-of relationship between doctors and patients
- GET: Check if given doctor is taking care of given patient
    - 200: if true
    - 404: if not
    - 403: permission request still on hold
'''
class TakeCareOfAPI(APIView):
    model = TakeCareOf
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)
    '''
    GET
    - Check if given doctor is taking care of given patient
        - 200: if true
        - 404: 
            - type=0: either the doctor or the patient doesn't exist. 
            - type=1: the relationship doesn't exist.
        - 409: permission request still on hold
        - 403: request is sent by neither the given doctor nor the given patient
    - Reponse:
        4XX:
            {
                "message": string
            }
        404:
            {
                "message": string,
                "type": int  [0 (user doesn't exist) / 1 (no permission)]
            }
        200:
            {
                "id": int,
                "doctor" : {
                    "id": UUID,
                    "first_name": String,
                    "last_name": String,
                    "since": DateTime,
                    "user_type": int,
                    "gender": int  
                },
                "patient" : {
                    "id": UUID,
                    "first_name": String, 
                    "last_name": String, 
                    "user_type": int,
                    "height": int, 
                    "weigh"': int, 
                    "date_of_birth": datetime, 
                    "notes": String, 
                    "phone": String,
                    "status": List<int>     
                }
            }
        
    '''
    def get(self, request, *args, **kwargs):
        # parsing request
        patient_id = kwargs['patient']
        doctor_id = kwargs['doctor']

        # check if given patients or doctors exists, return 404 if not so
        try:
            User.objects.get(id=patient_id)
            User.objects.get(id=doctor_id)
        except:
            return Response({"message": "Either doctor or patient doesn't eixst", "type":0}, status=404)

        # only given patient or given doctor can send the request. return 403 if not so
        accept_request = isSelf(request, patient_id) or isSelf(request, doctor_id)
        if(not accept_request):
            return Response({"message": "Request is sent by invalid users"}, status=403)
        
        # check if the data permission request is still on hold
        try:
            DataPermissionRequest.objects.get(doctor=doctor_id, patient=patient_id)
            return Response({"message": "Permission request is still on hold"}, status=409)
        except:
            pass

        # check if the takecareof relationship exists
        try:
            query = TakeCareof.objects.get(doctor=doctor_id, patient=patient_id)
            data = TakeCareOfSerializer(query).data
            return Response(data, status=200)
        except:
            return Response({"message": "You do not have the permission", "type":1}, status=404)

