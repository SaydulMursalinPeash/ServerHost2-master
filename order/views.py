from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from payment.models import Method
from accounts.renderers import *
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import AccessToken
from .models import Order
from django.views.decorators.csrf import csrf_exempt
from chat.models import *
'''
class OrderOrder(APIView):
    permission_classes=[AllowAny]
    renderer_classes=[UserRenderer]
    def post(self, request,format=None):
        access_token = request.GET.get('access_token')
        token_user=None
        if access_token is None:
            return Response({'error':'Access token is required.'},status=status.HTTP_400_BAD_REQUEST)
        token_obj=None
        try:
            token_obj=AccessToken.objects.get(token=access_token)
        except ObjectDoesNotExist as e:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        if token_obj is None:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        
        token_user=token_obj.user
        if token_user.id is not request.data.get('customer') and not token_user.is_admin:
            return Response({'error':'You are not Allowed to do this action.'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
'''
class Order(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def post(self, request,format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
class LatestUserOrder(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def get(self,request,user_uid,coin_id,format=None):
        user=None
        try:
            user= User.objects.get(id=user_uid)
        except ObjectDoesNotExist as e:
            return Response({'error':'You are not permitted to do this action. Sorry!'},status=status.HTTP_400_BAD_REQUEST)
        method=None
        try:
            method=Method.objects.get(id=coin_id)
        except ObjectDoesNotExist as e:
            return Response({'error':'Invalid coin.'},status=status.HTTP_400_BAD_REQUEST)

        if not user==request.user and not request.user.is_admin and not request.user.is_officer:
            return Response({'error':'You are not permitted to do this action. Sorry!'},status=status.HTTP_400_BAD_REQUEST)
        orders=Order.objects.filter(customer=user,coin=method)
        com_order=Order.objects.filter(customer=user,coin=method,state='complete')
        com=com_order.count()
        can=Order.objects.filter(state='cancel').count()
        icom=Order.objects.filter(customer=user,coin=method,state='processing').count()
        ser=AllOrdersSerializers(com_order,many=True)
        user_ser=UserSerializer(user)
        return Response({'user':user_ser.data,'data':ser.data,'num_comp':com,'num_incomp':icom,'num_cancel':can},status=status.HTTP_200_OK)


class EditOrderView(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def post(self,request,order_id,format=None):
        order=Order.objects.get(id=order_id)
        if not request.user.is_officer and not request.user.is_admin:
            return Response({'error':'You are not permitted to do this action.'},status=status.HTTP_400_BAD_REQUEST)
        state=request.data.get('state')
        order.state=state
        order.save()
        return Response({'msg':'Order state successfully changed to '+state+'.'},status=status.HTTP_200_OK)
    
class GetAllOrdersView(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def get(self,request):
        if not request.user.is_admin and not request.user.is_officer:
            return Response({'error':'You are not permitted to do this action.'},status=status.HTTP_400_BAD_REQUEST)
        orders=Order.objects.filter(state=True)
        com=Order.objects.filter(state='complete').count()
        icom=Order.objects.filter(state='processing').count()
        can=Order.objects.filter(state='cancel').count()
        serializer=OrderSerializer(orders,many=True)
        return Response({'msg':serializer.data,'num_comp':com,'num_incomp':icom,'num_cancel':can},status=status.HTTP_200_OK)


class BuyOrder(APIView):
    permission_classes=[AllowAny]
    def post(self,request,format=None):
        access_token = request.GET.get('access_token')
        token_user=None
        if access_token is None:
            return Response({'error':'Access token is required.'},status=status.HTTP_400_BAD_REQUEST)
        token_obj=None
        try:
            token_obj=AccessToken.objects.get(token=access_token)
        except ObjectDoesNotExist as e:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        if token_obj is None:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        
        token_user=token_obj.user
        
        
        serializer = BuyOrderSerializer(data=request.data,context={'user':token_user})
        if serializer.is_valid():
            #serializer.save()
            print('-----------------Ok-----------------------')
            user_order=Order.objects.filter(customer=token_user).order_by('-time').first()
            order_ser=AllOrdersSerializers(user_order)
            return Response(order_ser.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellOrder(APIView):
    permission_classes=[AllowAny]
    def post(self,request,format=None):
        access_token = request.GET.get('access_token')
        token_user=None
        if access_token is None or '':
            return Response({'error':'Access token is required.'},status=status.HTTP_400_BAD_REQUEST)
        token_obj=None
        try:
            token_obj=AccessToken.objects.get(token=access_token)
        except ObjectDoesNotExist as e:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        if token_obj is None:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        
        token_user=token_obj.user
        
        
        
        serializer = SellOrderSerializer(data=request.data,context={'user':token_user})
        if serializer.is_valid():
            #serializer.save()
            print('-----------------Ok-----------------------')
            user_order=Order.objects.filter(customer=token_user).order_by('-time').first()
            order_ser=AllOrdersSerializers(user_order)
            return Response(order_ser.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderStateChange(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request,id):
        if not request.user.is_admin:
            return Response({'error':'You are not permitted to do this action.'},status=status.HTTP_400_BAD_REQUEST)
       
        try:
            order_obj=Order.objects.get(id=id)
        except ObjectDoesNotExist as e:
            return Response({'error':'Invalid order Id.'},status=status.HTTP_400_BAD_REQUEST)
        order_obj.state=request.data.get('state')
        order_obj.save()
        cu_name=order_obj.customer.name
        or_method=order_obj.coin.name
        chat_room_name=cu_name+'_'+or_method
        chat_room_obj=ChatRoom.objects.get(name=chat_room_name)
        user_obj=request.user
        method_obj=order_obj.coin
        message=f"----------------------\nThe Order, ID: {order_obj.order_id} ({order_obj.amount} [{order_obj.method}] ) is closed Successfully. Thank you sir.\n--------------------------"
        Message.objects.create(message=message,user=user_obj,chat_room=chat_room_obj,method=method_obj)
        
        return Response({'msg':'Order state changet to Completed successfully.'},status=status.HTTP_200_OK)
    
class LatestUserIncompletedOrder(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def get(self,request,user_uid,coin_id,format=None):
        user=None
        try:
            user= User.objects.get(id=user_uid)
        except ObjectDoesNotExist as e:
            return Response({'error':'You are not permitted to do this action. Sorry!'},status=status.HTTP_400_BAD_REQUEST)
        method=None
        try:
            method=Method.objects.get(id=coin_id)
        except ObjectDoesNotExist as e:
            return Response({'error':'Invalid coin.'},status=status.HTTP_400_BAD_REQUEST)

        if not user==request.user and not request.user.is_admin and not request.user.is_officer:
            return Response({'error':'You are not permitted to do this action. Sorry!'},status=status.HTTP_400_BAD_REQUEST)
        orders=Order.objects.filter(customer=user,coin=method)
        incom_order=Order.objects.filter(customer=user,coin=method,state='processing')
        icom=incom_order.count()
        com=Order.objects.filter(customer=user,coin=method,state='complete').count()
        can=Order.objects.filter(customer=user,coin=method,state='cancel').count()
        ser=AllOrdersSerializers(incom_order,many=True)
        user_ser=UserSerializer(user)
        return Response({'user':user_ser.data,'data':ser.data,'num_comp':com,'num_incomp':icom},status=status.HTTP_200_OK)
