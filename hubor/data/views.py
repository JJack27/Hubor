'''
==== File Info ====
APIs which are data-related.
@author: Yizhou Zhao
@postDate: 2020/10/15 11:22
@lastUpdate: 2020/10/29 13:28

==== API Enclosed ====
- DataAPI
  /api/data/<uuid:pk>
    + GET: retrieve data of given uuid
    + POST: accepting uploaded data entries from given uuid
- VitalSignAPI
  /api/vs/<uuid:owner>/
    + GET: retireve vital signs of given uuid
    + POST: accpeting uploaded vital signs from given uuid
'''
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import uuid
import datetime
from dateutil import parser

# Project modules
from accounts.models import User, TakeCareOf
from data.models import *
from data.serializers import *


'''
/api/data/<uuid:pk>/
API for uplaoding and retrieving data entries. All users can perform this action
- POST
- GET
'''
class DataAPI(APIView):
    model = Data
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    POST
    - Accpeting data uploads from given uuid
    - payload:
        {
            bracelet: uuid,
            tem: double,
            acx: double,
            acz: double,
            bat: double,
            red: double,
            ir: double,
        }
    '''
    def post(self, request, *args, **kwargs):
        request_user = kwargs['pk']
        request_body = request.data
        response = {}
        # check if user exists
        if(str(request_user) != str(request.user.id)):
            return Response(response, status=403)

        request_body['owner'] = request_user
        serializer = DataSerializer(data = request_body)

        if(serializer.is_valid()):
            serializer.save()
            return Response(response, status=200)
        return Response(response, status=401)


    '''
    GET
    - Return a list of data of given user
    - return:
        {
            query: 'data',
            data:[
                {data_1},
                {data_2},
                ...
                {data_n}
            ]
        }
    '''
    def get(self, request, *args, **kwargs):
        owner = kwargs['pk']
        response = {'query': 'data', 'data':[]}
        
        # check authority of request user
        # only owner of the data and doctors/admins can access
        if(str(request.user.id) != str(owner) and request.user.user_type == 0):
            return Response (response, status=403)
    
        # get the data 
        query = Data.objects.filter(owner = owner).order_by('id')
        data = DataSerializer(query, many=True).data
        if(len(data) == 0):
            return Response(response, status = 404)
        response['data'] = data
        return Response(response, status=200)

'''
/api/vitalsign/<uuid:owner>/?from=<time_with_time_zone>&to=<time_with_time_zone>&type=['min', 'hr', 'day', 'month']
API for uplaoding and retrieving vital signs entries. All users can perform this action
- POST
- GET
'''
class VitalSignAPI(APIView):
    model = VitalSign
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    POST
    - Accpeting vital sign uploads from given uuid
    - payload:
        {
            bracelet: uuid,
            temp: double,
            spo2: double,
            hr: double,
            rr: double,
            [time: String,]
        }
    '''
    def post(self, request, *args, **kwargs):
        request_user = kwargs['owner']
        request_body = request.data
        response = {}
        
        # check if user exists
        if(str(request_user.id) != str(request.user.id)):
            return Response(response, status=403)

        request_body['owner'] = request_user
        serializer = VitalSignSerializer(data = request_body)

        if(serializer.is_valid()):
            serializer.save()
            return Response(response, status=200)
        return Response(response, status=401)


    '''
    GET
    - Return a list of vital signs of given user
    - return:
        {
            query: 'vitalsign',
            data:[
                {data_1},
                {data_2},
                ...
                {data_n}
            ]
        }
    '''
    def get(self, request, *args, **kwargs):
        # parsing the request
        owner = kwargs['owner']
        from_time = request.GET.get('from', None)
        to_time = request.GET.get('to', None)
        range_type = request.GET.get('type', None)
        print(from_time)
        print(to_time)
        print(range_type)
        
        # if the request is invalid, return status 400
        if(from_time == None or to_time == None or range_type == None):
            print("None in the request")
            return Response({}, status=400)
        
        # update from_time and to_time to datetime object
        try:
            from_time = parser.parse(from_time)
            to_time = parser.parse(to_time)
        except Exception as e:
            print(e)
            return Response({}, 400)
        
        # check authority of request user
        # only owner of the data and doctors/admins can access
        if(str(request.user.id) != str(owner) and request.user.user_type == 0):
            return Response ({}, status=403)
    
        # get the data 
        range_types = {'min':0, 'hr':1, 'day':2, 'month':3, 'year':4}
        query = AggregatedVitalSign.objects.filter(owner = owner, type=range_types[range_type], time__range=(from_time, to_time)).order_by('id')
        data = AggregatedVitalSignSerializer(query, many=True).data
        if(len(data) == 0):
            return Response({}, status = 404)
        return Response(data, status=200)


'''
/api/aggregatedvs/<uuid:owner>/
API for uplaoding and retrieving vital signs entries. All users can perform this action
- POST
- GET
'''
class AggregatedVitalSignAPI(APIView):
    model = AggregatedVitalSign
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        owner = User.objects.get(id=kwargs['owner'])
        range_types = {'min':0, 'hr':1, 'day':2, 'month':3, 'year':4}
        try:
            avs = AggregatedVitalSign(owner=owner, time = parser.parse(request.data['time']), type=range_types[request.data['type']], 
                temp_mean=request.data['temp_mean'], temp_min=request.data['temp_min'], temp_max=request.data['temp_max'], 
                temp_med=request.data['temp_med'], temp_std=request.data['temp_std'],
                hr_mean=request.data['hr_mean'], hr_min=request.data['hr_min'], hr_max=request.data['hr_max'], 
                hr_med=request.data['hr_med'], hr_std=request.data['hr_std'],
                rr_mean=request.data['rr_mean'], rr_min=request.data['rr_min'], rr_max=request.data['rr_max'], 
                rr_med=request.data['rr_med'], rr_std=request.data['rr_std'],
                spo2_mean=request.data['spo2_mean'], spo2_min=request.data['spo2_min'], spo2_max=request.data['spo2_max'], 
                spo2_med=request.data['spo2_med'], spo2_std=request.data['spo2_std'])
            
            avs.save()
            return Response({}, status=200)
        except Exception as e:
            print(e)
            return Response({}, status=400)

'''
/api/normalrange/<patient:uuid>/<type_range:string>/
API for uplaoding/creating and retrieving normal ranges
- PUT: Updating and creating a normal range
    - 400: request is invalid
    - 403: the request is forbidened
    - 200: success
'''
class NormalRangeAPI(APIView):
    model = NormalRange
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    '''
    PUT:
    - API for updating and creating an entry of a normal range
    - request:
        ```json
        {
            "value": number
        }
        ```
    - response:
        - 400: request is invalid
        - 403: the request is forbidened
        - 200: success
            ```json
            {
                "hr_l": number,
                "hr_h": number,
                "temp_l": number,
                "temp_h": number,
                "rr_l": number,
                "rr_h": number,
                "spo2_l": number,
                "spo2_h": number,
                "bp_l": number,
                "bp_h": number
            }
            ```
    '''
    def put(self, request, *args, **kwargs):
        # parsing the request
        request_body = request.data
        patient_id = kwargs['patient']
        patient = User.objects.get(id=patient_id)
        request_user = request.user
        type_range = kwargs['typerange'].split("_")
        if(len(type_range) != 2):
            return Response(status=400)
        vs = type_range[0]
        type_of_range = type_range[1]

        # check if vs and type_of_range is valid
        if(vs not in ["hr", "rr", "temp", "bp", "spo2"]):
            return Response(status=400)
        if(type_of_range not in ["h", "l"]):
            return Response(status=400)

        # check the validity of the value
        if(request_body['value'] < 0):
            return Response(status=400)

        # check authorization
        # check if the request is patient him/herself,
        #   if not, check if the requestor is having access to the patient's data
        if(patient != request_user):
            try:
                TakeCareOf.objects.get(doctor=request_user, patient=patient)
            except Exception as e:
                return Response(status=403)

        # check if given normal range exists
        try:
            normal_range = NormalRange.objects.get(patient=patient, vs=vs, type_of_range=type_of_range)
            normal_range.value = request_body['value']
            normal_range.save()
        except ObjectDoesNotExist:
            # create a new entry for given normal range
            normal_range = NormalRange(
                patient=patient,
                vs=vs,
                type_of_range=type_of_range,
                value=request_body['value']
            )
            normal_range.save()
        except:
            return Response(status=500)

        # return all the normal ranges of given patient
        data = NormalRangeSerializer(patient).data

        return Response(data, status=200)

'''
/api/allnormalrange/<uuid:patient>/
- GET: get all normal ranges of given patient
    - 404: given patient is not found or given patient has no normal ranges
    - 403: the request is forbidened
    - 200: success
'''
class AllNormalRangeAPI(APIView):
    model = NormalRange
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)
    
    '''
    GET:
    - get all normal ranges of given patient
    - response:
        - 404: given patient is not found or given patient has no normal ranges
        - 403: the request is forbidened
        - 200: success
            ```json
            {
                "hr_l": number,
                "hr_h": number,
                "temp_l": number,
                "temp_h": number,
                "rr_l": number,
                "rr_h": number,
                "spo2_l": number,
                "spo2_h": number,
                "bp_l": number,
                "bp_h": number
            }
            ```
    '''
    def get(self, request, *args, **kwargs):
        # parse the request
        try:
            patient = User.objects.get(id=kwargs['patient'])
        except:
            return Response(status=404)
        
        # check authorization
        # check if the request is patient him/herself,
        #   if not, check if the requestor is having access to the patient's data
        if(patient != request.user):
            try:
                TakeCareOf.objects.get(doctor=request.user, patient=patient)
            except Exception as e:
                return Response(status=403)
        
        # return all the normal ranges of given patient
        data = NormalRangeSerializer(patient).data
        return Response(data, status=200)

