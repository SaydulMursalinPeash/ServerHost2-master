from rest_framework import serializers,status
from .models import *

class MethodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Method
        fields='__all__'