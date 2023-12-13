from django.db import models
from accounts.models import User
from payment.models import Method
# Create your models here.


class ChatRoom(models.Model):
    name=models.CharField(max_length=300,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='chatroom_user')
    method=models.ForeignKey(Method,on_delete=models.CASCADE,related_name='chat_room_method')
    #stuff=models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='stuff_name')
    def __str__(self):
        return self.name



class Message(models.Model):
    message=models.TextField(max_length=3000,null=True)
    image=models.ImageField(default=None,null=True,upload_to='message/image/')
    #image=models.TextField(max_length=3000,null=True,blank=True,default=None)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_user')
    chat_room=models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name='chat_room_for_message')
    method=models.ForeignKey(Method,on_delete=models.CASCADE,null=True,related_name='message_method')
    time=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.user.name+' + '+self.chat_room.name  
    
class ChatRoomController(models.Model):
    chat_controller_name=models.CharField(max_length=200,null=True,blank=True)
    method=models.ForeignKey(Method,on_delete=models.CASCADE,related_name='controller_method')
    controller=models.ForeignKey(User,on_delete=models.CASCADE,related_name='controller_User')


    def __str__(self):
        return self.method.name+'( '+self.controller.name+' )'
