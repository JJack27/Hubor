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


class NormalRangeSerializer(serializers.ModelSerializer):
    hr_l = serializers.SerializerMethodField("get_hr_l")
    hr_h = serializers.SerializerMethodField("get_hr_h")
    rr_l = serializers.SerializerMethodField("get_rr_l")
    rr_h = serializers.SerializerMethodField("get_rr_h")
    temp_l = serializers.SerializerMethodField("get_temp_l")
    temp_h = serializers.SerializerMethodField("get_temp_h")
    spo2_l = serializers.SerializerMethodField("get_spo2_l")
    spo2_h = serializers.SerializerMethodField("get_spo2_h")
    bp_l = serializers.SerializerMethodField("get_bp_l")
    bp_h = serializers.SerializerMethodField("get_bp_h")

    def get_hr_l(self, obj):
        try:
            nr = NormalRange.objects.get(patient=obj, vs="hr", type_of_range="l")
            return nr.value
        except:
            return "null"
    
    def get_hr_h(self, obj):
        try:
            nr = NormalRange.objects.get(patient=obj, vs="hr", type_of_range="h")
            return nr.value
        except:
            return "null"

    def get_temp_l(self, obj):
        try:
            nr = NormalRange.objects.get(patient=obj, vs="temp", type_of_range="l")
            return nr.value
        except:
            return "null"

    def get_temp_h(self, obj):
        try:
            nr = NormalRange.objects.get(patient=obj, vs="temp", type_of_range="h")
            return nr.value
        except:
            return "null"

    def get_rr_l(self, obj):
        try:
            nr = NormalRange.objects.get(patient=obj, vs="rr", type_of_range="l")
            return nr.value
        except:
            return "null"

    def get_rr_h(self, obj):
        try:
            nr = NormalRange.objects.get(patient=obj, vs="rr", type_of_range="h")
            return nr.value
        except:
            return "null"

    def get_spo2_l(self, obj):
        try:
            nr = NormalRange.objects.get(patient=obj, vs="spo2", type_of_range="l")
            return nr.value
        except:
            return "null"

    def get_spo2_h(self, obj):
        try:
            nr = NormalRange.objects.get(patient=obj, vs="spo2", type_of_range="h")
            return nr.value
        except:
            return "null"
    
    def get_bp_l(self, obj):
        try:
            nr = NormalRange.objects.get(patient=obj, vs="bp", type_of_range="l")
            return nr.value
        except:
            return "null"

    def get_bp_h(self, obj):
        try:
            nr = NormalRange.objects.get(patient=obj, vs="bp", type_of_range="h")
            return nr.value
        except:
            return "null"

    class Meta:
        model = User
        fields= ['temp_h', 'temp_l', 'hr_h', 'hr_l', 'rr_h', 'rr_l', 'spo2_h', 'spo2_l', 'bp_h', 'bp_l']