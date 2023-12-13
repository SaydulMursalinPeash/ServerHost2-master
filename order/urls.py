from django.urls import path
from .views import *

urlpatterns = [
    path('create-order/buy/',BuyOrder.as_view(),name='create_order_buy'),
    path('get-user-order/<user_uid>/<coin_id>/',LatestUserOrder.as_view(),name='latest_user_order'),
    path('edit-order/<order_id>/',EditOrderView.as_view(),name='edit_order'),
    path('get-all-order/',GetAllOrdersView.as_view(),name='get_all_order'),
    path('create-order/sell/',SellOrder.as_view(),name='create_order_sell'),
    path('change-state/<int:id>/',OrderStateChange.as_view(),name='order-state-change'),
    path('get-user-incompleted-order/<user_uid>/<coin_id>/',LatestUserIncompletedOrder.as_view(),name='get_all_incompleted_order'),

]
