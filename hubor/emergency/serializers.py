from emergency.models import *
from rest_framework import serializers
from rest_framework.validator import Uniquevalidator
'''
Serializer for EmergencyContact
'''
class EmergencyContactSerializer(serializers.ModelSerializer):
    pass

'''
Serializer for EmergencyEvent
'''
class EmergencyEventSerializer(serializers.ModelSerializer):
    pass

'''
Serializer for EmergencyMessage
'''
class EmergencyMessageSerializer(serializers.ModelSerializer):
    pass