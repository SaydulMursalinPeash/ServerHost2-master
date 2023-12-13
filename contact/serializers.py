from rest_framework import serializers
from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError




class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=['email','name','subject','message']
    def create(self, validated_data):
        return Contact.objects.create(**validated_data)
    def validate(self,attrs):
        email=attrs.get('email')
        try:
            validate_email(email)
            print('Email is valid')
            return attrs
        except ValidationError:
            raise ValidationError("Invalid email.")
        return attrs