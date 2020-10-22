from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from configurations.models import *

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'