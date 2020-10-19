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
import datetime
from emergency.models import *
from emergency.serializers import *

'''
/api/emergency/<uuid:pk>/
Handle Emergency events of a given user with his/her UUID
- GET: Get a list of emergency events sent by given user
- POST: Initiate an emergency event
'''
class EmergencyEventAPI(APIView):
    model = EmergencyEvent    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    POST: initiate an emergency event
    - Request:
        {} - empty payload 
    - Response:
        {} - empty payload
    '''
    def post(self, request, *args, **kwargs):
        patient = kwargs['pk']

        # Check if request user has permission to access
        if(request.user.id != patient):
            return Response({}, status=403)
        
        # Check if given user exists
        try:
            patient_use = User.objects.get(id = patient)
        except:
            return Response({}, status=404)
        

        # add emergency events
        data = {'patient':patient}
        try:
            serializer = EmergencyEventSerializer(data=data)

            if (serializer.is_valid()):
                serializer.save()
                return Response({}, status=200)
        except:
            return Response({}, status=401)
        
        return Response({}, status=401)
    
    '''
    GET: get a list of emergency events by given user
    - response:
        {
            'data': [
                {emergency_1},
                {emergency_2},
                ...
                {emergency_3}
            ]
        }
    '''
    def get(self, request, *args, **kwargs):
        patient = kwargs['pk']

        # Check if request user has permission to access
        if(request.user.id != patient and request.user.user_type == 0):
            return Response({}, status=403)
        
        # Check if given user exists
        try:
            patient_use = User.objects.get(id = patient)
        except:
            return Response({}, status=404)

        # retrieve emergency events
        query = EmergencyEvent.objects.filter(patient=patient)
        
        data = EmergencyEventSerializer(query, many=True).data
        if (len(data) == 0):
            return Response({}, status=404)
        return Response({'data':data}, status=200)
        