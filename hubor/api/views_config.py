'''
==== File Info ====
APIs which are data-related.
@author: Yizhou Zhao
@postDate: 2020/10/22 11:40
@lastUpdate: 2020/10/29 13:51

==== API Enclosed ====
- ConfigurationAPI
  /api/config/<int:version>/
    + GET: Get the corresponding version of configuration
- LatestConfigAPI
  /api/latestconfig/
    + GET: Get the latest version of configuration
'''

from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import os
import uuid
import datetime

# Project modules
from accounts.models import User
from configurations.models import *
from configurations.serializers import *

'''
/api/config/<int:version>
    + GET: Get the corresponding version of configuration
'''
class ConfigurationAPI(APIView):
    model = Configuration

    '''
    GET: Get the corresponding version of configuration
    - Response:
        {
            config: [
                {
                    name: string,
                    version: int,
                    compare: int,
                    range_min: float,
                    range_max: float,
                    duration: int
                },
                {rule_2},
                ...
                {rule_n}
            ]
        }
    '''
    def get(self, request, *args, **kwargs):
        # Parsing the version number from the request
        try:
            version = int(kwargs['version'])
        except:
            return Response({}, status=401)

        # Getting all rules of given version
        query = Configuration.objects.filter(version=version)
        rules = ConfigurationSerializer(query, many=True).data
        if len(rules) == 0:
            return Response({}, status=404)
        
        response = {'config': rules}
        return Response(response, status=200)


'''
/api/latestconfig/
+ GET: Get the latest version of configuration
'''
class LatestConfigAPI(APIView):
    model = Configuration

    '''
    GET: Get the latest version of configuration
    - Response:
        {
            config: [
                {
                    name: string,
                    version: int,
                    compare: int,
                    range_min: float,
                    range_max: float,
                    duration: int
                },
                {rule_2},
                ...
                {rule_n}
            ]
        }
    '''
    def get(self, request, *args, **kwargs):
        # Getting the latest version number
        version = Configuration.objects.aggregate(Max('version'))['version__max']

        # Getting all rules of given version
        query = Configuration.objects.filter(version=version)
        rules = ConfigurationSerializer(query, many=True).data
        if len(rules) == 0:
            return Response({}, status=404)
        
        response = {'config': rules}
        return Response(response, status=200)

