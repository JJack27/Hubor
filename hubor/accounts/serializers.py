from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils import timezone
from accounts.models import *
from data.models import *
from data.serializers import *
import datetime
#class UserSerializer()

class BraceletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bracelet
        fields = '__all__'

class BaseUserSerializer(serializers.ModelSerializer):
    facility = serializers.SerializerMethodField('get_facility')

    def get_facility(self, obj):
        try:
            query = BelongsToFacilities.objects.get(user=obj.id)
            facility = query.facility
            return FacilitySerializer(facility).data
        except:
            return {'id': 'null'}

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_type', 'gender', 'facility', 
                    'date_joined', 'date_of_birth', 'phone', 'email']

class EmergencyUserSerializer(serializers.ModelSerializer):
    facility = serializers.SerializerMethodField('get_facility')

    def get_facility(self, obj):
        try:
            query = BelongsToFacilities.objects.get(user=obj.id)
            facility = query.facility
            return FacilitySerializer(facility).data
        except:
            return {'id': 'null'}

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_type', 'gender', 'facility']


class PatientStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientStatus
        fields = '__all__'


class ShortDoctorsSerializer(serializers.ModelSerializer):
    facility = serializers.SerializerMethodField('get_facility')

    def get_facility(self, obj):
        try:
            query = BelongsToFacilities.objects.get(user=obj.id)
            facility = query.facility
            return FacilitySerializer(facility).data
        except:
            return {'id': 'null'}

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name','facility']

'''
Serializer for patients
'''
class PatientSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='risk'
    )
    facility = serializers.SerializerMethodField('get_facility')
    hr = serializers.SerializerMethodField('get_hr')
    temp = serializers.SerializerMethodField('get_temp')
    rr = serializers.SerializerMethodField('get_rr')
    spo2 = serializers.SerializerMethodField('get_spo2')

    def get_hr(self, obj):
        try:
            query = VitalSign.objects.filter(owner=obj.id).latest('time')
            return VitalSignSerializer(query).data['hr']
        except:
            return 'null'

    def get_temp(self, obj):
        try:
            query = VitalSign.objects.filter(owner=obj.id).latest('time')
            return VitalSignSerializer(query).data['temp']
        except:
            return 'null'
    
    def get_rr(self, obj):
        try:
            query = VitalSign.objects.filter(owner=obj.id).latest('time')
            return VitalSignSerializer(query).data['rr']
        except:
            return 'null'

    def get_spo2(self, obj):
        try:
            query = VitalSign.objects.filter(owner=obj.id).latest('time')
            return VitalSignSerializer(query).data['spo2']
        except:
            return 'null'

    def get_facility(self, obj):
        try:
            query = BelongsToFacilities.objects.get(user=obj.id)
            facility = query.facility
            return FacilitySerializer(facility).data
        except:
            return {'id': 'null'}
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_type', 'height', 'weight', 'date_of_birth', 'notes', 'phone', 'status', 'facility',
            'hr', 'temp', 'rr', 'spo2', 'email']



class UserBelongsToSerializer(serializers.ModelSerializer):
    facility = serializers.SerializerMethodField('get_facility')
    user = serializers.SerializerMethodField('get_user')

    def get_facility(self, obj):
        try:
            query = Facilities.objects.get(id=obj.facility_id)
            facility = FacilitySerializer(query).data
            return facility
        except:
            return None
    
    def get_user(self, obj):
        query = User.objects.get(id=obj.user_id)
        user = EmergencyUserSerializer(query).data
        return user

    def validate(self, data):
        if(not isinstance(self.initial_data['user'], uuid.UUID)):
            raise serializers.ValidationError("'user' expect an UUID, get %s." % str(type(self.initial_data['user'])))
        if(not isinstance(self.initial_data['facility'], uuid.UUID)):
            raise serializers.ValidationError("'facility' expect an UUID, get %s." % str(type(self.initial_data['facility'])))
        
        return self.initial_data

    
    def update(self, instance, validated_data):
        instance.facility = Facilities.objects.get(id=validated_data.get('facility'))
        instance.user = User.objects.get(id=validated_data.get('user'))
        instance.since = timezone.now()
        instance.save()
        return instance

    def create(self, validated_data):
        # parse data
        facility = Facilities.objects.get(id=validated_data['facility'])
        user = User.objects.get(id=validated_data['user'])

        # save the relation
        relation = BelongsToFacilities.objects.create(facility=facility, user=user)  # pylint: disable=maybe-no-member

        #relation.save()
        return relation

    class Meta:
        model = BelongsToFacilities
        fields = ['id', 'user', 'facility']


'''
Serializer simply returns all fields of the facilities
'''
class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = '__all__'


class ExtendedFacilitySerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField('get_relations')

    def get_relations(self, obj):
        query = BelongsToFacilities.objects.filter(facility=obj.id)
        data = UserBelongsToSerializer(query, many=True).data
        return data

    class Meta: 
        model = Facilities
        fileds = ['id', 'name', 'address', 'phone', 'description', 'users']

class TakeCareOfSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField('get_doctor')
    patient = serializers.SerializerMethodField('get_patient')

    def get_doctor(self, obj):
        query = User.objects.get(id=obj.doctor_id)
        doctor = EmergencyUserSerializer(query).data
        return doctor
    
    def get_patient(self, obj):
        query = User.objects.get(id=obj.patient_id)
        patient = PatientSerializer(query).data
        return patient

    def validate(self, data):
        if(not isinstance(self.initial_data['doctor'], uuid.UUID)):
            raise serializers.ValidationError("'doctor' expect an UUID, get %s." % str(type(self.initial_data['doctor'])))
        if(not isinstance(self.initial_data['patient'], uuid.UUID)):
            raise serializers.ValidationError("'patient' expect an UUID, get %s." % str(type(self.initial_data['patient'])))
        
        return self.initial_data

    
    def update(self, instance, validated_data):
        instance.doctor = User.objects.get(id=validated_data.get('doctor'))
        instance.patient = User.objects.get(id=validated_data.get('patient'))
        instance.since = timezone.now()
        instance.save()
        return instance

    def create(self, validated_data):
        # parse data
        #print(validated_data)
        doctor = User.objects.get(id=validated_data['doctor'])
        patient = User.objects.get(id=validated_data['patient'])
        
        # save the relation
        relation = TakeCareOf.objects.create(doctor=doctor, patient=patient)  # pylint: disable=maybe-no-member
        #relation.save()
        return relation

    class Meta:
        model = TakeCareOf
        fields = ['id', 'doctor', 'patient']