import django
django.setup()
from accounts.models import User
from .models import Message,ChatRoom
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import datetime
from asgiref.sync import sync_to_async,async_to_sync
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import AccessToken
from payment.models import *
from django.core.exceptions import ObjectDoesNotExist
import base64 as base
from django.core.files.base import ContentFile
import binascii
from PIL import Image
import io

class ChatConsumer(AsyncWebsocketConsumer):
    def save_message_sync(user, message, chat_room):
        Message.objects.create(message=message,user=user, chat_room=chat_room)
    async def connect(self):
        #self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        #self.token = self.scope['url_route']['kwargs']['token']
        print('---------------------------------------------')
        self.room_object=await sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        self.room_email = await sync_to_async(str)(await sync_to_async(lambda: self.room_object.user)())
        self.room_user=await sync_to_async(User.objects.get)(email=self.room_email)
        # Get the token from the query parameters
        self.token = self.scope['query_string'].decode('utf-8')
        print(self.token)
        self.user=User()
        
        # Verify the token and get the user
        try:
            #self.user = token_obj.user
            self.token_object=await sync_to_async(AccessToken.objects.get)(token=self.token)
            self.user_email = await sync_to_async(str)(await sync_to_async(lambda: self.token_object.user)())
            self.user=await sync_to_async(User.objects.get)(email=self.user_email)


            #self.user=self.token_object.user
        except Token.DoesNotExist as e:
            # Close the connection if the token is invalid
            print('Peash')
            await self.close()




        if not self.user.is_authenticated:
            print('not_authenticated')
            await self.close()


        # Check if user is the designated user or an admin
        if not self.user.is_staff and (self.room_user.name!=self.user.name):
            #print(self.room_user.name)
            #print(self.user.name)
            print('-------------------------------')
            await self.close()

        name = self.room_name
        self.room_group_name = f'chat_{name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print('Disconnected')
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        #text_data_json = json.loads(text_data)
        #message = text_data_json['message']

        # Check if user is authenticated and has permission to send messages
        '''if not self.user.is_authenticated or (not self.user.is_staff and self.user.username != "designated_user"):
            await self.close()'''
        
        if not self.user.is_staff and (self.room_user.name!=self.user.name):
            await self.close()
            if not text_data:
                return

        try:
            print(text_data)
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            print(message)
        except (json.JSONDecodeError, KeyError):
            print('error')
            return
        await sync_to_async(Message.objects.create)(user=self.user, message=message,chat_room=self.room_object)
        # Save message to database
        #Message.objects.create(user=self.user, message=message,chat_room=self.room_object)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'chat_room':{'name':self.room_name},
                'message': message,
                'time':str(datetime.datetime.now()),
                'user':{
                    'id':self.user.id,
                    'name':self.user.name
                }
            }
        )

    async def chat_message(self, event):
        message = event

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class ChatMethodConsumer(AsyncWebsocketConsumer):
    def save_message_sync(user, message, chat_room):
        Message.objects.create(message=message,user=user, chat_room=chat_room)
    async def connect(self):
        print('entered------------------------------------')
        #self.user = self.scope["user"]
        self.method_name=self.scope['url_route']['kwargs']['method_name']
        self.room_name = self.scope['url_route']['kwargs']['user_name']+'_'+self.method_name
        
        #self.token = self.scope['url_route']['kwargs']['token']
        print('---------------------------------------------')


        
        
        
        # Get the token from the query parameters
        self.token = self.scope['query_string'].decode('utf-8')
        print(self.token)
        self.user=User()
        
        if self.token is None or '':
            print('Invalid Token.')
            await self.close()
        
        # Verify the token and get the user
        try:
            #self.user = token_obj.user
            self.token_object=await sync_to_async(AccessToken.objects.get)(token=self.token)
            self.user_email = await sync_to_async(str)(await sync_to_async(lambda: self.token_object.user)())
            self.user=await sync_to_async(User.objects.get)(email=self.user_email)
            self.method=await sync_to_async(Method.objects.get)(name=self.method_name)


            #self.user=self.token_object.user
        except Token.DoesNotExist as e:
            # Close the connection if the token is invalid
            print('Peash')
            await self.close()

        self.room_object=None
        try:
            self.room_object=await sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        
        except ObjectDoesNotExist as e:
            self.room_object=await sync_to_async(ChatRoom.objects.create)(name=self.room_name, user=self.user,method=self.method)
            
        self.room_email = await sync_to_async(str)(await sync_to_async(lambda: self.room_object.user)())
        link_user=None
        self.room_user=await sync_to_async(User.objects.get)(email=self.room_email)
        try:
            self.link_user=await sync_to_async(User.objects.get)(name=self.scope['url_route']['kwargs']['user_name'])
        except ObjectDoesNotExist as e:
            self.link_user=None
            print('-----------------------------user not found---------------------------------')



        if not self.user.is_authenticated:
            print('not_authenticated')
            await self.close()

        if(self.link_user==None):
            print('-------------------Closed-----------------')
            await self.close()
        # Check if user is the designated user or an admin
        if not self.user.is_staff and (self.room_user.name!=self.user.name) and not self.user.is_officer and not self.user==self.link_user:
            #print(self.room_user.name)
            #print(self.user.name)
            await self.close()
        else:
            print('--------------------------Ok')

        name = self.room_name
        self.room_group_name = f'chat_{name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print('Disconnected')
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        #text_data_json = json.loads(text_data)
        #message = text_data_json['message']

        # Check if user is authenticated and has permission to send messages
        '''if not self.user.is_authenticated or (not self.user.is_staff and self.user.username != "designated_user"):
            await self.close()'''
        text_img=''
        if not self.user.is_staff and (self.room_user.name!=self.user.name):
            await self.close()
            if not text_data:
                return

        try:
            #print(text_data)
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            text_img=text_data_json['image']
            
            print(message)
            if text_img =='':
                await sync_to_async(Message.objects.create)(user=self.user, message=message,image=None,chat_room=self.room_object,method=self.method)
            else:
                try:
                    text_img4=text_img.split(',')[1]
                    msg_img2=base.b64decode(text_img4)
                    current_time = datetime.datetime.now()
                    current_milliseconds = str(current_time.timestamp() * 1000)
                    filename='img'+ str(current_milliseconds)+'.png'
                    image_file=ContentFile(msg_img2,name=filename)
                    await sync_to_async(Message.objects.create)(user=self.user, message=message,image=image_file,chat_room=self.room_object,method=self.method)
                    print('Image saved...................******')
                except binascii.Error as e:
                    print("***************Not Image. Just Text.")
                    await sync_to_async(Message.objects.create)(user=self.user, message=message,image=None,chat_room=self.room_object,method=self.method)
                

            #print(message)
        except (json.JSONDecodeError, KeyError):
            print('error')
            return
        
        #await sync_to_async(Message.objects.create)(user=self.user, message=message,image=None,chat_room=self.room_object,method=self.method)
        
        #await sync_to_async(Message.objects.create)(user=self.user, message=message,image=image_file,chat_room=self.room_object,method=self.method)
        # Save message to database
        #Message.objects.create(user=self.user, message=message,chat_room=self.room_object)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'chat_room':{'name':self.room_name},
                'message': message,
                'image':text_img,
                'time':str(datetime.datetime.now()),
                'user':{
                    'id':self.user.id,
                    'name':self.user.name
                }
            }
        )

    async def chat_message(self, event):
        message = event

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))




'''

try:
                msg_img1 = text_data_json['image']
                msg_img=msg_img1
                msg_img2=base.b64decode(msg_img)
                image_file=ContentFile(msg_img2)
                await sync_to_async(Message.objects.create)(user=self.user, message=message,image=image_file,chat_room=self.room_object,method=self.method)
                print('Image saved...................******')
            except binascii.Error as e:
                print("***************Not Image. Just Text.")
                await sync_to_async(Message.objects.create)(user=self.user, message=message,image=None,chat_room=self.room_object,method=self.method)
'''