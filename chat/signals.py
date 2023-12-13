import pusher
from .models import Message
from django.core.signals import request_started
from django.dispatch import receiver
from django.db.models.signals import post_save
from order.models import Order
from django.utils import timezone
from django.utils.timesince import timesince

pusher_client = pusher.Pusher(
  app_id='1644457',
  key='910b862b7b97cf8e6d72',
  secret='3d01355215785e2b46a0',
  cluster='ap2',
  ssl=True
)

@receiver(post_save, sender=Message)
def send_message_notification(sender, instance, **kwargs):
    created_at_datetime = instance.time

    current_time = timezone.now()
    time_difference = timesince(created_at_datetime, current_time)
    message = f"New Message from - User: {instance.user.name} for Coin: {instance.chat_room.method.name} - Time: {time_difference} ago."
    pusher_client.trigger('my-channel', 'my-event', {'message': message})

@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, **kwargs):
    message = f"New Order: {instance.coin.name} - Amount: {instance.amount}"
    pusher_client.trigger('my-channel', 'my-event', {'message': message})
