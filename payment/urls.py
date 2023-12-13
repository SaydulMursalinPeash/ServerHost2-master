from django.urls import path
from .views import *

urlpatterns = [
    path('all-method/',GetAllMethod.as_view(),name='get_all_method'),
    path('single-method/<uid>/',GetSingleMethod.as_view(),name='get_single_method')
]
