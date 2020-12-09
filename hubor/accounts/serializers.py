from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import *
import datetime
#class UserSerializer()

class BraceletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bracelet
        fields = '__all__'

class EmergencyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_type']


class TakeCareOfSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField('get_doctor')
    patient = serializers.SerializerMethodField('get_patient')

    def get_doctor(self, obj):
        query = User.objects.get(id=obj.doctor_id)
        doctor = EmergencyUserSerializer(query).data
        return doctor
    
    def get_patient(self, obj):
        query = User.objects.get(id=obj.patient_id)
        patient = EmergencyUserSerializer(query).data
        return patient

    def validate(self, data):
        if(not isinstance(self.initial_data['doctor'], uuid.UUID)):
            raise serializers.ValidationError("'doctor' expect an UUID, get %s." % str(type(self.initial_data['doctor'])))
        if(not isinstance(self.initial_data['patient'], uuid.UUID)):
            raise serializers.ValidationError("'patient' expect an UUID, get %s." % str(type(self.initial_data['patient'])))
        
        return self.initial_data

    
    def update(self, instance, validated_data):
        print(validated_data)
        instance.doctor = User.objects.get(id=validated_data.get('doctor'))
        instance.patient = User.objects.get(id=validated_data.get('patient'))
        instance.since = datetime.datetime.now()
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