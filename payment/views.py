from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


class GetAllMethod(APIView):
    def get(self,request,format=None):
        methods=Method.objects.all()
        serializers=MethodSerializer(methods,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    

class GetSingleMethod(APIView):
    def get(self,request,uid,format=None):
        try:
            method=Method.objects.get(id=uid)
            serializers=MethodSerializer(method)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({'error':'Invalid Method Id.'},status=status.HTTP_400_BAD_REQUEST)

