from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import *
from rest_framework import response,status
from django.core.exceptions import ObjectDoesNotExist


class AllCurrency(APIView):
    def get(self,request,format=None):
      cur=Currency.objects.all()
      serializer=CurrencySerializer(cur,many=True)  
      print(cur)
      return Response({'msg':serializer.data},status=status.HTTP_200_OK)
    
class SingleCurrency(APIView):
   def get(self,request,uid,format=None):
      try:
        cur=Currency.objects.get(id=uid)
        serializer=CurrencySerializer(cur)
        return Response(serializer.data,status=status.HTTP_200_OK)
      except ObjectDoesNotExist as e:
         return Response({'error':'Invalid Currency Id.'},status=status.HTTP_400_BAD_REQUEST)



