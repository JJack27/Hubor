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
    bp_h = serializers.SerializerMethodField('get_bp_h')
    bp_l = serializers.SerializerMethodField('get_bp_l')
    def get_temp(self, obj):
        return {
            'mean': obj.temp_mean,
            'med': obj.temp_med,
            'min': obj.temp_min,
            'max': obj.temp_max,
            'std': obj.temp_std
        }

    def get_hr(self, obj):
        return {
            'mean': obj.hr_mean,
            'med': obj.hr_med,
            'min': obj.hr_min,
            'max': obj.hr_max,
            'std': obj.hr_std
        }

    def get_rr(self, obj):
        return {
            'mean': obj.rr_mean,
            'med': obj.rr_med,
            'min': obj.rr_min,
            'max': obj.rr_max,
            'std': obj.rr_std
        }

    def get_spo2(self, obj):
        return {
            'mean': obj.spo2_mean,
            'med': obj.spo2_med,
            'min': obj.spo2_min,
            'max': obj.spo2_max,
            'std': obj.spo2_std
        }

    def get_bp_h(self, obj):
        return {
            'mean': obj.bp_h_mean,
            'med': obj.bp_h_med,
            'min': obj.bp_h_min,
            'max': obj.bp_h_max,
            'std': obj.bp_h_std
        }
    
    def get_bp_l(self, obj):
        return {
            'mean': obj.bp_l_mean,
            'med': obj.bp_l_med,
            'min': obj.bp_l_min,
            'max': obj.bp_l_max,
            'std': obj.bp_l_std
        }

    class Meta:
        model = AggregatedVitalSign
        fields = ['time', 'temp', 'hr', 'rr', 'spo2', 'bp_h', 'bp_l']