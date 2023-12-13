from django.db import models

class Method(models.Model):
    name=models.CharField(max_length=300,null=False,blank=False,unique=True)
    buy_rate=models.FloatField(null=True)
    sell_rate=models.FloatField(null=True)
    description=models.TextField(max_length=500,null=True,blank=True)
    icon=models.ImageField(upload_to='payment/method/')

    def __str__(self):
        return self.name
