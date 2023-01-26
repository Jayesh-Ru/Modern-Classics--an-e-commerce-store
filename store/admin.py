from django.contrib import admin
from .models import Category, Product, Customer, Order              #new

# Register your models here.

#details for django to tell it what models we want to access through admin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','category_image']
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','brand','slug','price','in_stock','is_active','created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price','in_stock']
    prepopulated_fields ={'slug':('title',)}