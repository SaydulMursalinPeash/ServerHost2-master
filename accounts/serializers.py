from rest_framework import serializers
from accounts.models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util



class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesn't match!")
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','is_admin','is_officer']


class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model =User
        fields=['email','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name','is_officer','is_admin']


class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2']
    def validate(self,attrs):
        pass1=attrs.get('password')
        pass2=attrs.get('password2')
        user=self.context.get('user')
        if pass1!=pass2:
            raise serializers.ValidationError("Password and Confirm password doesn't match.")
        user.set_password(pass1)
        user.save()
        return attrs
    


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('Password reset Token: ',token)
            link='https://ptopuser-h2u4.vercel.app/api/user/reset-password/'+uid+'/'+token+'/'
            print('Password reset link: ',link)
            data={
                'subject':'Reset password.',
                'body':'Click following link to reset password '+link,
                'to_email':user.email
            }
            Util.send_email(data)
            print('----------------------------------')
            return attrs
        else:
            raise serializers.ValidationError('Your Email is not valid.')

        
class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2']
    def validate(self,attrs):
        try:
            pass1=attrs.get('password')
            pass2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            user=self.context.get('user')
            if pass1!=pass2:
                raise serializers.ValidationError("Password and Confirm password doesn't match.")
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token=token):
                raise serializers.ValidationError("Token is not valid or Expired.")
            
            user.set_password(pass1)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("Token is not valid or Expaired.")

class UserEmailVarificationSerializer(serializers.Serializer):
    def validate(self,attrs):
        try:
            uid=self.context.get('uid')
            token=self.context.get('token')
            user=self.context.get('user')
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token=token):
                raise serializers.ValidationError("Token is not valid or Expired.")

            user.is_valid=True
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("Token is not valid or Expaired.")




     