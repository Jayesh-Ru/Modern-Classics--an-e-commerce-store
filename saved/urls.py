from django.urls import path
from . import views

app_name='saved'

urlpatterns = [
    path('wishlist/', views.wishlist, name='wishlist'),
    path('saved/', views.add_item, name='saved'),

]