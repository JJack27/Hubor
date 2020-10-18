from emergency.models import *
from rest_framework import serializers
from rest_framework.validator import Uniquevalidator
'''
Serializer for EmergencyContact
'''
class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'

''' 
Serializer for EmergencyEvent
'''
class EmergencyEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyEvent
        fields = '__all__'

'''
Serializer for EmergencyMessage
'''
class EmergencyMessageSerializer(serializers.ModelSerializer):
    pass