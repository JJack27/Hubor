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

'''
================ HELPER FUNCTIONS ================
'''
# is the request is sent by given id
def isSelf(request, id) -> bool:
    return request.user.id == id

# is the request is sent by him/herself or by a staff
def isSelfOrStaff(request, id) -> bool:
    # check if this request is authorized.
    # - only doctors, admins, and patient himself can post
    return request.user.user_type == 1 or request.user.user_type == 2 or request.user.id == id

'''
================ END HELPER FUNCTIONS ================
'''


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
            if(user.user_type == 0):
                status = PatientStatus(patient = user, risk=0)
                status.save()
            return Response(response, status=200)
        except Exception as e:
            print(e)
            return Response(response, status=401)
    
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
    - response:
        {
            query: bracelet,
            bracelet: UUID of new added bracelet
        }
    '''
    def post(self, request, *args, **kwargs):
        owner = kwargs['owner']
        request_body = request.data
        request_body['owner'] = owner
        response = {'query':'bracelet'}
        response['bracelet'] = {}
        # validate if user exist
        try:
            r_owner = User.objects.get(id=owner)
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


'''
/api/takecareof/<UUID:doctor>/<UUID:patient>/
API Represents the take-care-of relationship between doctors and patients
Note that this API isn't responsible for updating the relationship
'''
class TakeCareOfAPI(APIView):
    model = TakeCareOf
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    POST
    - Create a take-care-of relationship between given doctors and patients
    - payload:
        {} - Empty payload
    - return:
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
        - 200: relationship created
        - 403: forbidden
        - 404: didn't find given doctor or patient
        - 409: when given patient is already assigned to a doctor
    '''
    def post(self, request, *args, **kwargs):
        # parsing reqeust
        doctor_id = kwargs['doctor']
        patient_id = kwargs['patient']
        body = {'doctor':doctor_id, 
                'patient':patient_id
                }
        
        # check if this request is authorized.
        # - only doctors, admins, and patient himself can post
        if(not isSelfOrStaff(request, patient_id)):
            return Response({}, status=403)

        # check if given doctor and given patient exists
        try:
            patient_user = User.objects.get(id=doctor_id, user_type=1)
            User.objects.get(id=patient_id, user_type=0)
        except:
            return Response({}, status=404)

        try:
            TakeCareOf.objects.get(patient=patient_user)
            return Response({}, status=409)
        except:
            pass

        # save the relationship into the database
        try:
            serializer = TakeCareOfSerializer(data=body)
            if(serializer.is_valid()):
                #print("validated data: ", serializer.validated_data)
                relation = serializer.save()
                data = TakeCareOfSerializer(relation).data
                return Response(data, status=200)
            else:
                return Response({}, status=400)
        except Exception as e:
            print(e)
            return Response({}, status=400)


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
            print('relation with given patient does not exist')
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

        # check authorization
        if(not isSelfOrStaff(request, doctor_id)):
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

            data = EmergencyUserSerializer(query, many=True).data
            return Response(data, status=200)
        except Exception as e:
            print(e)
            return Response([], status=400)

            