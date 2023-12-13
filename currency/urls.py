from django.urls import path
from .views import *


urlpatterns = [
    path('all-currency/',AllCurrency.as_view(),name='get_all_currency'),
    path('single-currency/<uid>/',SingleCurrency.as_view(),name='get_single_currency')
]
