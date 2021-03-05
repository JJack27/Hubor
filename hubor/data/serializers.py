from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from data.models import *

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'

class VitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSign
        fields = '__all__'


class AggregatedVitalSignSerializer(serializers.ModelSerializer):
    temp = serializers.SerializerMethodField('get_temp')
    hr = serializers.SerializerMethodField('get_hr')
    rr = serializers.SerializerMethodField('get_rr')
    spo2 = serializers.SerializerMethodField('get_spo2')
    
    def get_temp(self, obj):
        return {
            'mean': obj.temp_mean,
            'mid': obj.temp_mid,
            'min': obj.temp_min,
            'max': obj.temp_max,
            'std': obj.temp_std
        }

    def get_hr(self, obj):
        return {
            'mean': obj.hr_mean,
            'mid': obj.hr_mid,
            'min': obj.hr_min,
            'max': obj.hr_max,
            'std': obj.hr_std
        }

    def get_rr(self, obj):
        return {
            'mean': obj.rr_mean,
            'mid': obj.rr_mid,
            'min': obj.rr_min,
            'max': obj.rr_max,
            'std': obj.rr_std
        }

    def get_spo2(self, obj):
        return {
            'mean': obj.spo2_mean,
            'mid': obj.spo2_mid,
            'min': obj.spo2_min,
            'max': obj.spo2_max,
            'std': obj.spo2_std
        }

    class Meta:
        model = AggregatedVitalSign
        fields = ['time', 'temp', 'hr', 'rr', 'spo2']