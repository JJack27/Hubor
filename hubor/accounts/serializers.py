from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import *

class BraceletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bracelet
        fields = '__all__'

class EmergencyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']