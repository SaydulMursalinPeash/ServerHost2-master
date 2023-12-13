from django.db import models
from accounts.models import *
from payment.models import *
from currency.models import *
from random import random


def generate_random_digits(length):                                                 #Generate random digits of the specified length.

    from random import randint
    return ''.join(str(randint(0, 9)) for _ in range(length))


def generate_unique_order_id(prefix):
    user_id = f"{prefix}{generate_random_digits(10)}"
    while Order.objects.filter(order_id=user_id).exists():
        user_id = f"{prefix}{generate_random_digits(10)}"
   
    return user_id


class Order(models.Model):
    order_id=models.CharField(max_length=15, unique=True,null=True)
    customer=models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='order_customer')
    account_details=models.TextField(max_length=2000,null=True,blank=True)
    coin=models.ForeignKey(Method,null=True,on_delete=models.CASCADE,related_name='order_method')
    amount=models.FloatField(null=True,blank=True)
    order_email=models.EmailField(null=True,blank=True)
    purpose=models.CharField(max_length=200,default='pay',null=True,blank=True)
    trc20_address=models.CharField(max_length=300,null=True,blank=True,default=None)
    bep20_address=models.CharField(max_length=300,null=True,blank=True,default=None)
    method=models.CharField(max_length=200,null=True,blank=True)
    state=models.CharField(max_length=10,null=True,default='processing')
    time=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            pre='ORD'
            
            id=generate_unique_order_id(pre)
            #print('---------------------------')
            self.order_id = id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer.name + ' '+self.order_id

