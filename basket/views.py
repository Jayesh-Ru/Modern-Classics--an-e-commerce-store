from django.shortcuts import render,get_object_or_404
from .basket import Basket
from store.models import Product
from django.http import JsonResponse
from account.models import UserBase

# Create your views here.
def basket_summary(request):
    try:
        user = UserBase.objects.get(user_name = request.user.user_name)
        if user.is_subscribed:
            result = 'yes' 
        else:
            result = 'no'                                                           #without [0]...we were getting a queryset but by specifying the position we are getting an object
    except:
        result='no'
    basket=Basket(request)                                                      #from the query set. This is not correct logic as when the user isn't subscribed this will give an
    print(result)                                                               # IndexError 
    return render(request, 'basket/summary.html',{'result':result})

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        
        basketqty= basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        discount = basket.discount()
        discountedprice = basket.get_discounted_price()
        basketqty = basket.__len__()
        subtotal = basket.get_subtotal_price()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': subtotal, 'total':baskettotal, 'discount':discount,'discounted_price':discountedprice})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)
        
        discount = basket.discount()
        discountedprice = basket.get_discounted_price()
        basketqty = basket.__len__()
        subtotal = basket.get_subtotal_price()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': subtotal, 'total':baskettotal, 'discount':discount,'discounted_price':discountedprice})
        return response