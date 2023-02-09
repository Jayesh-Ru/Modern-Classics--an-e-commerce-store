from django.shortcuts import get_object_or_404,render
from decimal import Decimal

# Create your views here.
from account.models import UserBase
from .models import Category,Product,Order,Customer

def product_all(request):
    products = Product.products.all()          #new
    return render(request, 'store/index.html',{'products':products})


def product_detail(request, slug):
    products_at_discount= get_object_or_404(Product, slug=slug, in_stock=True)
    original= get_object_or_404(Product, slug=slug, in_stock=True)
    user = UserBase.objects.get(user_name = request.user.user_name)
    if user.is_subscribed:
        result = 'yes' 
        print('yes')
        products_at_discount.price = products_at_discount.price *Decimal(0.9)
    else:
        result = 'no'   
    return render(request,'store/single.html',{'product':products_at_discount,'original':original,'result':result})

def category_list(request, category_slug=None):
    category = get_object_or_404(Category,slug=category_slug)
    products_at_discount = Product.objects.filter(category=category)
    original = Product.objects.filter(category=category)
    user = UserBase.objects.get(user_name = request.user.user_name)
    if user.is_subscribed:
        result = 'yes'
        for i in products_at_discount:
         i.price = i.price *Decimal(0.9)
    else:
        result = 'no'   

    return render(request, 'store/category.html',{'category':category,'original':original, 'products':products_at_discount,'result':result})

def about(request):
    return render(request, 'store/about.html')

def subscribe_section(request):
    return render(request,'store/subscribe_section.html')

def contact_section(request):
    return render(request,'store/contactus.html')