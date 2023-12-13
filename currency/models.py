from django.db import models

class Currency(models.Model):
    name=models.CharField(max_length=200,unique=True,null=False,blank=False)
    symbol=models.CharField(max_length=50,unique=True,null=False,blank=True)
    description=models.TextField(max_length=500,null=True,blank=True)
    icon=models.ImageField(upload_to='currency/icons')
    buy_rate=models.FloatField()
    sell_rate=models.FloatField()
    def __str__(self):
        return self.name


