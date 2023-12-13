from django.core.mail import EmailMessage
from payment.models import Method
from chat.models import ChatRoomController
from accounts.models import User
import os
class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email='saydulpeash428@gmail.com',
            to=data['to_email']

        )
        email.send()
    @staticmethod
    def get_sub_emails(method):
        method_object=Method.objects.get(name=method)
        controller_objects=ChatRoomController.objects.filter(method=method_object)
        officers=[]
        #print('-----------------------------saua')
        for i in controller_objects:
            officers.append(i.controller)
            
        admins=User.objects.filter(is_admin=True)
        list4=[]

        for i in range(len(officers)):
            list4.append(officers[i].email)
        for i in range(len(admins)):
            list4.append(admins[i].email)
            
        return list4