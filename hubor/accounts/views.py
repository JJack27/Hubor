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
# Create your views here.




'''
Get basic information of current logged in user
'''
class MyInfoAPI(APIView):
    model = User
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    GET
    - Get basic information of current logged in user
    - Response
        {
            "id": UUID,
            "first_name": String,
            "last_name": String,
            "date_joined": DateTime,
            "user_type": int,
            "gender": int,
            "facility": <facility>,
            "phone": String,
            "email": String
        }
    '''
    def get(self, request, *args, **kwargs):
        # see if requesting user is anonymous
        try:
            id = request.user.id
        except:
            return Response({}, status=403)
        
        data = BaseUserSerializer(request.user).data
        return Response(data, status=200)


        

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
    - response:
        {
            query: bracelet,
            bracelet: UUID of new added bracelet
        }
    '''
    def post(self, request, *args, **kwargs):
        owner = kwargs['owner']
        request_body = dict(request.data)
        request_body['owner'] = owner
        response = {'query':'bracelet'}
        response['bracelet'] = {}

        # validate if user exist
        try:
            owner = User.objects.get(id=owner)
        except:
            return Response(response, status=404)
        
        # validate mac_addr
        try:
            valid = re.search('^([0-9A-Faf]{2}[:-]){5}([0-9A-Faf]{2})$', request_body['mac_addr'])
            if valid:
                serializer = BraceletSerializer(data = request_body)
                if(serializer.is_valid()):
                    bracelet = serializer.save()
                    response['bracelet'] = BraceletSerializer(bracelet).data
                    
                    return Response(response, status=200)
                
            return Response(response, status=400)
        except Exception as e:
            print(e)
            return Response(response, status=400)
    
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



'''
/api/doctorof/<UUID:patient>/
Get the doctor's information of given patient
- GET: Get the doctor's information of given patient
- PUT: Update the TakeCareOf relationship.
'''
class DoctorOfAPI(APIView):
    model = TakeCareOf
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    GET
    - Get the doctor's information of the given patient
    - Response:
        {
            id: UUID,
            first_name: String, 
            last_name: String, 
            user_type: int
        }
    '''
    def get(self, request, *args, **kwargs):
        # parse the request
        patient_id = kwargs['patient']

        '''
        # Deprecated: patients may not belongs to any of the health care facilities
        # check authorization. Only the staff and patients belongs to the facility can get this information
        try:
            fa_of_request = BelongsToFacilities.objects.get(user=request.user).facility_id
            fa_of_patient = BelongsToFacilities.objects.get(user=patient_id).facility_id
            assert fa_of_patient == fa_of_request, "User belongs to different facilities"
        except:
            return Response({}, status=403)
        '''

        # check authorization
        if(not isSelfOrStaff(request, patient_id)):
            return Response({}, status=403)
        
        # check if take-care-of relationship of given patient exists
        try:
            patient_user = User.objects.get(id = patient_id)
            relation = TakeCareOf.objects.get(patient=patient_user)
            doctor_user = relation.doctor
        except:
            return Response({}, status=404)

        # serializing the TakeCareOf object
        try:
            doctor_data = EmergencyUserSerializer(doctor_user).data
            return Response(doctor_data, status=200)
        except:
            return Response({}, status=400)

    '''
    PUT
    @ Deprecated
    - Update the doctor user takeCareOf relationship of given patient. 
    - Payload:
        {
            doctor_id: UUID/String
        }
    - Response:
        {
            "id": int,
            "doctor" : {
                "id": UUID,
                "first_name": String,
                "last_name": String,
                "since": DateTime,
                "user_type": int    
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
        - 404: unable to find given given doctor
        - 403: request is not sent by the patient him/herself, nor by doctors and admins
    '''
    '''
    def put(self, request, *args, **kwargs):
        # parse the request
        patient_id = kwargs['patient']
        doctor_id = request.data['doctor_id']
        try:
            body = {'doctor':uuid.UUID(doctor_id), 
                'patient':patient_id
                }
        except:
            return Response({}, status=400)

        
        # Deprecated: patients may not belongs to any of the health care facilities
        # check authorization. Only the staff and patients belongs to the facility can get this information
        try:
            fa_of_request = BelongsToFacilities.objects.get(user=request.user).facility_id
            fa_of_doctor = BelongsToFacilities.objects.get(user=uuid.UUID(doctor_id)).facility_id
            fa_of_patient = BelongsToFacilities.objects.get(user=patient_id).facility_id
            assert fa_of_doctor == fa_of_request, "User belongs to different facilities"
            assert fa_of_patient == fa_of_request, "User belongs to different facilities"
        except:
            return Response({}, status=403)
        

        # check authorization
        if(not isSelfOrStaff(request, patient_id)):
            return Response({}, status=403)
        
        # check if given doctor and given patient exists
        try:
            patient_user = User.objects.get(id=patient_id, user_type=0)
            User.objects.get(id=doctor_id, user_type=1)
            
        except:
            return Response({}, status=404)

        # check if relation with patient exists
        try:
            relation = TakeCareOf.objects.get(patient=patient_user)
            serializer = TakeCareOfSerializer(relation, data=body)
        except:
            # if not exist, create one
            serializer = TakeCareOfSerializer(data=body)
        
        # save the relationship into the database
        try:
            if(serializer.is_valid()):
                relation = serializer.save()
                data = TakeCareOfSerializer(relation).data
                return Response(data, status=200)
            else:
                #print(relation)
                print("data is invalid")
                return Response({}, status=400)
        except Exception as e:
            print(e)
            return Response({}, status=400)
    '''

'''
/api/patientsof/<UUID:doctor>/
Get the patients' information of a given doctor
- GET: Get the patients' information of a given doctor
'''
class PatientsOfAPI(APIView):
    model = TakeCareOf
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    GET
    - Get the patients' information of a given doctor
    - Response:
            [
                {
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
                },
                {
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
            ]
    '''
    def get(self, request, *args, **kwargs):
        # parse the request
        doctor_id = kwargs['doctor']
        '''
        # Deprecated: patients may not belongs to any of the health care facilities
        # check authorization. Only the staff and patients belongs to the facility can get this information
        try:
            fa_of_request = BelongsToFacilities.objects.get(user=request.user).facility_id
            fa_of_doctor = BelongsToFacilities.objects.get(user=doctor_id).facility_id
            assert fa_of_doctor == fa_of_request, "User belongs to different facilities"
        except:
            return Response({}, status=403)
        '''
        
        # check authorization
        if(not isStaff(request)):
            return Response({}, status=403)
        
        # check if take-care-of relationship of given patient exists
        try:
            doctor_user = User.objects.get(id = doctor_id)
            relations = TakeCareOf.objects.filter(doctor=doctor_user)
            if(len(relations) == 0):
                return Response({}, status=404)
            patient_users = []
            for relation in relations:
                patient_users.append(relation.patient)
        except:
            return Response({}, status=404)

        # serializing the TakeCareOf object
        try:
            patients_data = PatientSerializer(patient_users, many=True).data
            return Response(patients_data, status=200)
        except:
            return Response({}, status=400)


'''
/api/doctors/
Get the doctor's information of given patient
- GET: Get a list of current doctors
''' 
class DoctorsAPI(APIView):
    model = User
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    GET
    - Response:
        [
            {
                "id": UUID,
                "first_name": String,
                "last_name": String,
                "since": DateTime,
                "user_type": int  
            },
            {
                "id": UUID,
                "first_name": String,
                "last_name": String,
                "since": DateTime,
                "user_type": int  
            }
        ]
    '''
    def get(self, request, *args, **kwargs):
        try:
            # setting up the query
            query = User.objects.filter(user_type=1)
            '''
            valid_query = []
            for doctor in query:
                try:
                    BelongsToFacilities.objects.get(user=doctor.id)
                    valid_query.append(doctor)
                except:
                    pass
            '''
            data = EmergencyUserSerializer(query, many=True).data
            return Response(data, status=200)
        except Exception as e:
            print(e)
            return Response([], status=400)


'''
/api/shortdoctors/
Get the patients' information of a given doctor
- GET: Get the patients' information of a given doctor
'''
class ShortDoctorsAPI(APIView):

    '''
    GET
    - Response:
        [
            {
                "id": UUID,
                "first_name": String,
                "last_name": String,
            },
            {
                "id": UUID,
                "first_name": String,
                "last_name": String,
            }
        ]
    '''
    def get(self, request, *args, **kwargs):
        try:
            # setting up the query
            query = User.objects.filter(user_type=1)
            '''
            valid_query = []
            for doctor in query:
                try:
                    BelongsToFacilities.objects.get(user=doctor.id)
                    valid_query.append(doctor)
                except:
                    pass
            '''
            data = EmergencyUserSerializer(query, many=True).data
            return Response(data, status=200)
        except Exception as e:
            print(e)
            return Response([], status=400)


'''
/api/facities/
- GET: Get a all facilities. Only short information included
- POST: Create a facility.
'''
class FacilitiesAPI(APIView):
    model = User
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    GET
    - Get a list of facilities
    - Response
        [
            {
                "id": UUID,
                "name": String,
                "address": String,
                "phone": String,
                "Description": String
            },
            {
                "id": UUID,
                "name": String,
                "address": String,
                "phone": String,
                "Description": String
            }
        ]
    '''
    def get(self, request, *args, **kwargs):
        try:
            query = Facilities.objects.all()
            data = FacilitySerializer(query, many=True).data
            return Response(data, status=200)
        except Exception as e:
            print(e)
            return Response({}, status=400)

    '''
    POST
    - Create a facility
    - Payload:
        {
            "id": UUID,
            "name": String,
            "address": String,
            "phone": String,
            "Description": String
        }
    - Resposne"
        {
            "id": UUID,
            "name": String,
            "address": String,
            "phone": String,
            "Description": String
        }
    '''
    def post(self, request, *args, **kwargs):
        # Check the authorization of the request user
        if(not isStaff(request)):
            return Response({}, status=403)
        
        # Parse the payload
        request_body = request.data

        try:
            serializer = FacilitySerializer(data = request_body)
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data, status=200)
            raise Exception("Invalid data")
        except Exception as e:
            print(e)
            return Response({}, status=400)


'''
/api/belongsto/<uuid:facility>
- GET: Get a all user belongs to given facility
- PUT: Create a belongs to relationship
'''
class BelongsToAPI(APIView):
    model = User
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    GET
    - Get a all user belongs to given facility
    - Response
        [
            {
                "id": UUID,
                "user": {
                    'id': UUID, 
                    'first_name': String, 
                    'last_name': String, 
                    'user_type': int, 
                    'gender': int, 
                    'belongs_to': UUID
                },
                "facility":{
                    "id": UUID,
                    "name": String,
                    "address": String,
                    "phone": String,
                    "Description": String
                }
            },
            ...
        ]
    '''
    def get(self, request, *args, **kwargs):
        facility = kwargs['facility']
        # check authorization. Only the staff and patients belongs to the facility can get this information
        try:
            query = BelongsToFacilities.objects.get(facility=facility, user=request.user)
        except:
            return Response({}, status=403)

        # getting data
        try:
            query = BelongsToFacilities.objects.filter(facility=facility)
            data = UserBelongsToSerializer(query, many=True).data
            return Response(data, status=200)
        except Exception as e:
            print(e)
            return Response({}, status=400)

    '''
    PUT
    - Create a belongs to relationship
    - Payload:
        {
            "user": UUID
        }
    - Resposne"
        {
            "id": UUID,
            "user": {
                'id': UUID, 
                'first_name': String, 
                'last_name': String, 
                'user_type': int, 
                'gender': int, 
                'belongs_to': UUID
            },
            "facility":{
                "id": UUID,
                "name": String,
                "address": String,
                "phone": String,
                "Description": String
            }
        }
    '''
    def put(self, request, *args, **kwargs):
        # Check the authorization of the request user
        if(not isSelfOrStaff(request, uuid.UUID(request.data['user']))):
            return Response({}, status=403)
        
        # Parse the payload
        body = {
            'facility': kwargs['facility'],
            'user': uuid.UUID(request.data['user'])
        }

        # see if given user was assigned to a health facility
        try:
            query = BelongsToFacilities.objects.get(user = body['user'])
            serializer = UserBelongsToSerializer(query, data=body)
        except:
            serializer = UserBelongsToSerializer(data=body)

        try:
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data, status=200)
            raise Exception("Invalid data")
        except Exception as e:
            print(e)
            return Response({}, status=400)
