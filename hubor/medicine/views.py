from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import os


# Create your views here.
'''
Return a list of autocomplete options
'''
class AllMedicinesAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            print(os.getcwd())
            path = os.path.join(os.getcwd(), "media/json/autocomplete/drugs.json")
            file = open(path)
            
        except Exception as e:
            print(e)
            return Response({}, status=404)
        response = json.load(file)
        return Response(response, status=200)