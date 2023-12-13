from django.urls import path
from .views import *



urlpatterns = [
    path('create-contact/',ContactView.as_view(),name='add_contact')
]
