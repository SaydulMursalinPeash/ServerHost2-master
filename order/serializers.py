from rest_framework import serializers
from rest_framework import response
from accounts.models import *
from payment.models import *
from .models import *
from currency.models import *
from chat.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name']

class OrderSerializer(serializers.ModelSerializer):
    customer=UserSerializer()

    class Meta:
        model = Order
        fields = ['order_id','customer','account_details', 'coin', 'amount', 'method','state']


class BuyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['account_details', 'coin', 'amount','purpose','order_email', 'method']
    def validate(self, attrs):
        #cu=User.objects.get(id=attrs.get('customer'))
        ad=attrs.get('account_details')
            #co=Method.objects.get(id=attrs.get('coin'))
            
        am=attrs.get('amount')
        oe=attrs.get('order_email')
        pu=attrs.get('purpose')
        me=attrs.get('method')

        order=Order.objects.create(
            customer=self.context.get('user'),
            account_details=ad,
            coin=attrs.get('coin'),
            amount=am,
            purpose=pu,
            order_email=oe,
            method=me,
        )
        order_obj=order
        cu_name=order_obj.customer.name
        or_method=order_obj.coin.name
        chat_room_name=cu_name+'_'+or_method
        chat_room_obj=ChatRoom.objects.get(name=chat_room_name)
        user_obj=order.customer
        method_obj=order_obj.coin
        message=f"++++++++++++++++++++++\nNew Order\n\nOrder ID: {order_obj.id}({order_obj.method})\nCoin: {order_obj.coin.name}\nAmount: {order_obj.amount}\nAccount Details: {order_obj.account_details}\nOrder Email: {order_obj.order_email}\n is Placed Successfully.\n++++++++++++++++++++++++++"
        Message.objects.create(message=message,user=user_obj,chat_room=chat_room_obj,method=method_obj)
        print('-----create_ok___-')
        return order   


class SellOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['account_details', 'coin', 'amount','trc20_address','bep20_address', 'method']
    def validate(self, attrs):
        #cu=User.objects.get(id=attrs.get('customer'))
        ad=attrs.get('account_details')
            #co=Method.objects.get(id=attrs.get('coin'))
        am=attrs.get('amount')
        trc=attrs.get('trc20_address')
        bep=attrs.get('bep20_address')
        me=attrs.get('method')

        order=Order.objects.create(
            customer=self.context.get('user'),
            account_details=ad,
            coin=attrs.get('coin'),
            amount=am,
            purpose=None,
            trc20_address=trc,
            bep20_address=bep,
            method=me,

        )
        order_obj=order
        cu_name=order_obj.customer.name
        or_method=order_obj.coin.name
        chat_room_name=cu_name+'_'+or_method
        chat_room_obj=ChatRoom.objects.get(name=chat_room_name)
        user_obj=order.customer
        method_obj=order_obj.coin
        message=f"++++++++++++++++++++++\nNew Order,\n\nOrder ID: {order_obj.order_id} ({order_obj.method}) \nCoin: {order_obj.coin.name}\nAmount: {order_obj.amount}\nAccount Details: {order_obj.account_details}\nOrder Email: {order_obj.order_email}\n is Placed Successfully.\n++++++++++++++++++++++++++"
        Message.objects.create(message=message,user=user_obj,chat_room=chat_room_obj,method=method_obj)
        print('-----create_ok___-')
        return order 

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model=Method
        fields=['id','name','icon']  
        
           
class AllOrdersSerializers(serializers.ModelSerializer):
    customer=UserSerializer()
    coin=CoinSerializer()
    class Meta:
        model=Order
        fields=['id','order_id','customer','account_details','coin','amount','order_email','purpose','trc20_address','bep20_address','method','state','time']