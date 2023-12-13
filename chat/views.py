from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .renderers import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from .renderers import *
from rest_framework.permissions import AllowAny
from accounts.models import AccessToken
class RoomMessage(APIView):
    permission_classes=[AllowAny]
    def get(self,request,room_name,format=None):
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

        
        try:
            room = ChatRoom.objects.get(name=room_name)
            messages = room.chat_room_for_message.all()
            serializer=MessageSerializer(messages,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({'msg':'Chat not found.'},status=status.HTTP_200_OK)





'''
class RoomMessage(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def get(self,request,room_name,fromat=None):
        room=ChatRoom.objects.get(name=room_name)
        if request.user.name!=room.user.name and not request.user.is_admin and not request.user.is_officer:
            return Response({'error':'You are not allowed to view this chats.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            room = ChatRoom.objects.get(name=room_name)
            messages = room.chat_room_for_message.all()
            serializer=MessageSerializer(messages,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({'error':'Invalid chat.'},status=status.HTTP_400_BAD_REQUEST)

'''


def get_chat_rooms_ordered_by_last_message_time():
    # Get all the ChatRoom objects
    chat_rooms = ChatRoom.objects.all()

    # Annotate each ChatRoom object with the timestamp of its latest message
    chat_rooms = chat_rooms.annotate(last_message_time=Max('chat_room_for_message__time'))

    # Sort the ChatRoom objects by their latest message timestamp in descending order
    chat_rooms = chat_rooms.order_by('-last_message_time')

    return chat_rooms

class AllChatRooms(APIView):
    permission_classes=[IsAuthenticated,IsAdminUser]
    renderer_classes=[UserRenderer]
    def get(self,request,fromat=None):
        ordered_chatrooms=get_chat_rooms_ordered_by_last_message_time()
        serializer=ChatRoomSerializer(ordered_chatrooms,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ChatMethodRooms(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        user=request.user
        if user.is_admin or user.is_officer:
            chat_controllers=ChatRoomController.objects.filter(controller=user)
            related_methods = []
            for chat_controller in chat_controllers:
                related_methods += list(chat_controller.method_set.all())
            # Assuming `related_methods` is a list of Method objects
            related_chatrooms = ChatRoom.objects.filter(method__in=related_methods)
            chat_rooms = related_chatrooms.annotate(last_message_time=Max('chat_room_for_message__time'))

        # Sort the ChatRoom objects by their latest message timestamp in descending order
            chat_rooms = chat_rooms.order_by('-last_message_time')
            serializer=ChatRoomSerializer(chat_rooms,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'error':'Sorry! You are not admin or Officer.'},status=status.HTTP_400_BAD_REQUEST)

class AllOfficers(APIView):
    rendere_classes=[UserRenderer]
    permission_classes=[IsAuthenticated,IsAdminUser]
    def get(self,request,format=None):
        all_officers=User.objects.filter(is_officer=True)
        serializer=UserSerializer(all_officers,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AddOfficerRole(APIView):
    rendere_classes=[UserRenderer]
    permission_classes=[IsAuthenticated,IsAdminUser]
    def post(self,request,format=None):
        method_name=request.data.get('method')
        method=Method.objects.get(name=method_name)
        controller_name=request.data.get('controller')
        controller=User.objects.get(name=controller_name)
        chat_controller=ChatRoomController.objects.create(method=method,controller=controller)
        return Response({'msg':controller_name +' is added to '+method_name},status=status.HTTP_200_OK)




        