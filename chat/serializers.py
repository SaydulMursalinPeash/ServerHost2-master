from rest_framework import serializers
from rest_framework import response
from .models import *
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','is_admin','is_officer']
class ChatRoomSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=ChatRoom
        fields=['name','user']

class MessageSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    chat_room=ChatRoomSerializer()
    class Meta:
        model=Message
        fields=['message','image','user','chat_room','time']
    def to_representation(self, instance):
            server_address='https://p2p-server-l9qu.onrender.com/'
            data = super().to_representation(instance)
            if data.get('image'):
                image_url = f"{server_address}{data['image']}"
                data['image'] = image_url
            return data