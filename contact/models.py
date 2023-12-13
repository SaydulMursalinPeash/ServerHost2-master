from django.db import models

class Contact(models.Model):
    email=models.EmailField(max_length=500,null=True,blank=True)
    name=models.CharField(max_length=250,null=True,blank=True)
    
    subject=models.TextField(max_length=500,null=True,blank=True)
    message=models.TextField(max_length=2000,null=True)

    def __str__(self):
        return self.email