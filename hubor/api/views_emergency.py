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
from accounts.models import *
from accounts.serializers import *
#from channels.layers import get_channel_layer
#from asgiref.sync import async_to_sync
from configurations.models import Configuration
from configurations.serializers import ConfigurationSerializer
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
        {
            "longitude": float,
            "latitude": float,
            "configuration": int,
            "risk": int,
            ["time": String]
        } 
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
             User.objects.get(id = patient)
        except:
            return Response({}, status=404)
        

        # add emergency events
        data = request.data
        data['patient'] = patient
        status_data = {"patient": patient}
        status_data['risk'] = data['risk']
        try:
            serializer = EmergencyEventSerializer(data=data)
            status_query = PatientStatus.objects.get(patient=patient)
            status_serializer = PatientStatusSerializer(status_query,data=status_data)
            if (serializer.is_valid() and status_serializer.is_valid()):
                serializer.save()
                status_serializer.save()
                '''
                # Send notification through channel layer
                group_name = "0"
                channel_layer = get_channel_layer()
                
                # Parsing emergency event
                data = serializer.data
                query = User.objects.get(id=data['patient'])
                patient_data = EmergencyUserSerializer(query).data
                query = Configuration.objects.get(id=data['configuration'])
                config_data = ConfigurationSerializer(query).data

                data['configuration'] = config_data
                data['patient'] = patient_data
                data = json.dumps(data)
                async_to_sync(channel_layer.group_send)(group_name, {'type':'notification_message', 'data':data})
                '''
                return Response({}, status=200)
        except Exception as e:
            print(e)
            return Response({}, status=400)
        
        return Response({}, status=400)
    
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
            User.objects.get(id = patient)
        except:
            return Response({}, status=404)

        # retrieve emergency events
        query = EmergencyEvent.objects.filter(patient=patient) # pylint: disable=maybe-no-member
        
        data = EmergencyEventSerializer(query, many=True).data
        if (len(data) == 0):
            return Response({}, status=404)
        return Response(data, status=200)

'''
/api/emergencycontact/<uuid:pk>/
Handle Emergency contacts of a given user with his/her UUID
- GET: Get a list of emergency contacts of given user
- POST: Create an emergency contact for given user
'''
class EmergencyContactAPI(APIView):
    model = EmergencyContact    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    GET: Get a list of emergency contacts of given user
    - response:
        {
            'data': [
                {emergency_contact_1},
                {emergency_contact_2},
                ...
                {emergency_contact_3}
            ]
        }
    '''
    def get(self, request, *args, **kwargs):
        patient = kwargs['pk']
        response = {"query": "emergencycontact"}
        # Check if request user has permission to access
        if(request.user.id != patient and request.user.user_type == 0):
            return Response({}, status=403)
        
        # Check if given user exists
        try:
            User.objects.get(id = patient)
        except:
            return Response({}, status=404)
        
        # Get a list of emergency contacts
        query = EmergencyContact.objects.filter(patient=patient)
        contacts = EmergencyContactSerializer(query, many=True).data

        if(len(contacts) == 0):
            return Response({}, status=404)
        else:
            response['data'] = contacts
            return Response(response, status=200)
