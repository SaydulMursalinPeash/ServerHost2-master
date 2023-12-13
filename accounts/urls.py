from django.urls import path
from .views import *
from chat.views import RoomMessage
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',UserChangePasswordView.as_view(),name='change_password'),
    path('send-reset-password-email/',SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='user-password-reset'),
    path('varify-email/<uid>/<token>/',UserEmailVarificationView.as_view(),name='user-email-varify'),
    path('messages/<room_name>/',RoomMessage.as_view(),name='get_messagessssss'),
    
]
