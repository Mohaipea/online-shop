from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.add_user_order, name='order'),
    path('openorder/', views.open_order, name='openorder'),
    path('remove_order/<order_id>', views.remove_order, name='remove_order'),
    path('request/', views.send_request, name='request'),
    path('verify/<orderid>', views.verify, name='verify'),
]