from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import Util
from chat.models import ChatRoom
from .models import Order

@receiver(post_save, sender=Order)
def notify_admins(sender, instance, created, **kwargs):
    util=Util()
    if created:
        order=instance
        order_user=order.customer.name
        order_coin=order.coin.name
        order_amount=order.amount
        order_email=order.order_email

        emails=Util.get_sub_emails(order_coin)
        data={

            'subject':'Order Update',
                'body':f"""

                    Name : {order_user}
                    Coin  : {order_coin}
                    Order Email : {order_email}
                    Amount : {order_amount}                        

                """,
                'to_email':emails
            }
        Util.send_email(data)

