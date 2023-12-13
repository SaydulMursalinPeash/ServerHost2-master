from rest_framework import serializers
from rest_framework import response
from .models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model=Currency
        fields=['id','name','symbol','description','icon','buy_rate','sell_rate']