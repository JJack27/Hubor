'''
==== File Info ====
APIs which are data-related.
@author: Yizhou Zhao
@postDate: 2020/10/15 11:22
@lastUpdate: 2020/10/15 11:22

==== API Enclosed ====
- DataAPI
  /api/data/<uuid:pk>
    + GET: retrieve data of given uuid
    + POST: accepting uploaded data entries from given uuid
- GetAllDataAPI
  /api/alldata/
    + GET: retrieve all data
'''
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import uuid
import datetime

# Project modules
from accounts.models import User
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