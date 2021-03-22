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
            DataPermissionRequest.objects.get(owner=patient_id, requestor=doctor_id)
            return Response({"message": "Permission request is still on hold"}, status=409)
        except :
            pass

        # check if the takecareof relationship exists
        try:
            query = TakeCareOf.objects.get(doctor=doctor_id, patient=patient_id)
            data = TakeCareOfSerializer(query).data
            return Response(data, status=200)
        except:
            return Response({"message": "Access not granted", "type":1}, status=404)
    
    '''
    DELETE
    - Remove a given TakeCareOf relationship
    - Method can only be used by given patient or doctor
    - Response:
        - status code:
            - 200: succeed
            - 403: requestor is neither the given patient nor the doctor
            - 404: the relationship between given patient and the doctor is not found.
                   Or the given patient or the given doctor doens't exist
        - response:
            ```json
            {
                "message": string
            }
            ```
    '''
    def delete(self, request, *args, **kwargs):
        # parsing the request
        patient_id = kwargs['patient']
        doctor_id = kwargs['doctor']

        # validate authorization
        if(patient_id != request.user.id and doctor_id != request.user.id):
            return Response({"message": "Permission denied"}, status=403)
        
        # check if given patient and doctor exists
        try:
            User.objects.get(id=patient_id)
            User.objects.get(id=doctor_id)
        except:
            return Response({"message": "Given doctor or patient doesn't exist"}, status=404)

        # check if the relationship exists
        # if so, delete it
        # otherwise, return 404
        try:
            query = TakeCareOf.objects.get(patient=patient_id, doctor=doctor_id)
            query.delete()
            return Response({"message": "Succeed"}, status=200)
        except:
            return Response({"message": "Relathionship doesn't exist"}, status=404)

'''
/api/accessrequest/<uuid:owner>/<uuid:requestor>/
- API allows requestor to send a request to the data owner so that he/she can access the vital sign data
- POST
    - requestor can be both requestor and the onwer.
        - Requestor POST: asking for the access.
        - Owner POST: Accept the request. this will delete the DataPermissionRequest tuple, but will create a 
          TakeCareOf object instead. If there is not existing request, then a TakeCareOf object will be created
          directly.
    - payload:
      ```json
        {
          "message": string
        }
      ```
    - Response:
        - 200: the request is sent or the TakeCareOf is created
        - 404: either the requestor or the owner doesn't exist
        - 409: the request already exist in the database and the post is sent by the reqeustor not the owner
- DELETE
    - Reject or cancel the request
    - Status Code:
        - 200: the request is rejected.
        - 403: the requestor is neither the owner nor the requestor
        - 404: given request is not found
'''
class AccessRequestAPI(APIView):
    model = TakeCareOf
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    POST
    - Allows requestor to send a request to the data owner so that he/she can access the vital sign data
        - 200: the request is sent or the TakeCareOf is created
        - 404: either the requestor or the owner doesn't exist
        - 409: the request already exist in the database and the post is sent by the reqeustor not the owner.
               Or the request is sent by the owner, but there is no existing entry in the database.
    - Reponse:
        4XX:
            {
                "message": string
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
    def post(self, request, *args, **kwargs):
        # parsing the request
        owner_id = kwargs["owner"]
        requestor_id = kwargs["requestor"]
        

        # make sure the person who sent request is one of owner or requestor
        if(owner_id != request.user.id and requestor_id != request.user.id):
            return Response({"message":"Permission denied"}, status=403)

        # check if the owner exists.
        # if not, return 404
        try:
            owner = User.objects.get(id=owner_id)
            requestor = User.objects.get(id=requestor_id)
        except:
            return Response({"message": "The user you are requesting doesn't exist"}, status=404)

        # check if the takeCareOf relationship already exists,
        # if so, return 409
        try:
            TakeCareOf.objects.get(patient=owner_id, doctor=requestor_id)
            return Response({"message": "access already granted"}, status=409)
        except:
            pass

        # check if there is already a request tuple. 
        #   if so, check if the request is sent the owner
        #       if so, return create a TakeCareOf object and save it to the database, return 200
        #   if not (not sent by the owner and already eixst), return 409
        try:
            request_entry = DataPermissionRequest.objects.get(owner=owner, requestor=requestor)
            
            # if this request made by the owner, delete the existing request entry (later will handle the creation of the TakeCareOf object)
            if(request.user.id == owner_id):
                request_entry.delete()
            else:
                return Response({"message": "The request has already been sent"}, status=409)
        except:
            pass

        # if this post is made by owner, directly create a TakeCareOf object
        if(request.user.id == owner_id):
            take_care_of_obj = TakeCareOf.objects.create(patient=owner, doctor=requestor)
            take_care_of_obj.save()
            data = TakeCareOfSerializer(take_care_of_obj).data
            return Response(data, status=200)

        # create a DataPermissionRequest object
        # return 200
        request_obj = DataPermissionRequest(owner=owner, requestor=requestor)
        request_obj.save()
        data = DataPermissionRequestSerializer(request_obj).data
        return Response(data, status=200)


    '''
    DELETE
    - Reject or cancel the request
    - Status Code:
        - 200: the request is rejected.
        - 403: the requestor is neither the owner nor the requestor
        - 404: given request is not found
    - Response
        {
            "message": string
        }
    '''
    def delete(self, request, *args, **kwargs):
        # parsing the request
        owner_id = kwargs["owner"]
        requestor_id = kwargs["requestor"]
        
        # if the person who sent request is the owner
        # if not, return 403
        if(request.user.id != owner_id and request.user.id != requestor_id):
            return Response({"message":"Permission denied"}, status=403)
    
        # check if the given request exists
        # if not, return 404
        try:
            data_request = DataPermissionRequest.objects.get(owner=owner_id, requestor=requestor_id)
        except:
            return Response({"message": "Given request is not found"}, status=404)

        # delete the entry (reject the request)
        data_request.delete()
        return Response({"message": "Succeed"}, status=200)

'''
/api/mypendingrequests/
- API allows user to get a list of their pending requests
- GET
    - Get a list of their pending requests
    - Response:
        - status codes:
            - 200: Response with a list of pending requests
            - 404: no pending requests found
        - response:
            ```json
            200:[
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
                    },
                    ...
                ]
            400:{
                "message": string
            }
            ```
'''
class MyPendingRequestsAPI(APIView):
    model = TakeCareOf
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # filtering the requests
        # if user is a patient
        if(request.user.user_type == 0):
            query = DataPermissionRequest.objects.filter(owner=request.user.id)
        else:
            query = DataPermissionRequest.objects.filter(requestor=request.user.id)

        # serialize the data
        data = DataPermissionRequestSerializer(query, many=True).data
        if(len(data) == 0):
            return Response(data, status=404)
        return Response(data, status=200)