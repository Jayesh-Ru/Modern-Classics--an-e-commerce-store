from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('',views.product_all,name='product_all'),
    path('about/',views.about,name='about'),
    path('subscribe_section/',views.subscribe_section,name='subscribe_section'),
    path('contact/',views.contact_section,name='contact_us'),
    path('new_arrival/',views.new_arrival,name='new_arrival'),   
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/<slug:category_slug>/', views.category_list, name='category_list'),
    
    
]
