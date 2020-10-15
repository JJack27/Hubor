from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import *

class BraceletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bracelet
        fields = '__all__'