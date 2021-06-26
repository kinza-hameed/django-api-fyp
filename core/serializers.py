from django.core.validators import MaxLengthValidator
from rest_framework import serializers
from core.models import *

class FileSerializer(serializers.Serializer):
	file = serializers.ImageField()

class PatientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patient
		fields = '__all__'

class MedicalTestSerializer(serializers.ModelSerializer):
	class Meta:
		model = MedicalTest
		fields = '__all__'

class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=25)