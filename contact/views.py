from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import *
from rest_framework.response import Response
from rest_framework import status

from .utils import *

class ContactView(APIView):
    def post(self,request,format=None):
        serializer=ContactUsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=request.data.get('email')
            name=request.data.get('name')
            subject=request.data.get('subject')
            message=request.data.get('message')
            data_confirmation={
                'subject':'Confirmation of receiving your email.',
                'body':f"""
Dear {name},

We wanted to let you know that we have received your email. Thank you for taking the time to write to us.

We are currently reviewing the message you sent and will respond as soon as possible. If we need any further information, we will reach out to you.

Thank you again for contacting us.

Best regards,
[PtoP Team.]""",
                'to_email':email
            }

            data_to_us={
                'subject':subject,
                'body':f"""
From: {email}

{message}

Best regards,
{name}.
""",
                'to_email':'saydulpeash019@gmail.com'
            }
            Util.send_email(data_confirmation)
            Util.send_email(data_to_us)
            serializer.save()
            return Response({'msg':'Your message has been sent.'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)