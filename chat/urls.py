from django.urls import path
from .views import *

urlpatterns = [
    
    path('chat-rooms/',AllChatRooms.as_view(),name='get_all_chat_rooms'),
    path('chat-method-rooms/',ChatMethodRooms.as_view(),name='chat_method_rooms'),
    path('all-officers/',AllOfficers.as_view(),name='get-all-officers'),
    path('add-officer-role/',AddOfficerRole.as_view(),name='add-officer-roll'),

]
