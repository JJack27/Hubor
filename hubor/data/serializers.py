from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from data.models import *

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'