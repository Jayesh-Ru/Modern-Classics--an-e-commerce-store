from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.BasketView, name='basket'),
    path('order_confirmation/', views.BasketView, name='basket'),
    # path('order_cancellation/', views.orderCancelled, name='order_cancelled'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('error/', views.Error.as_view(), name='error'),
    path('webhook/', views.stripe_webhook),
]