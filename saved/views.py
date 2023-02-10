from django.shortcuts import render,get_object_or_404
from store.models import Product
from django.http import JsonResponse
from basket.basket import Basket
# Create your views here.


def wishlist(request):
    products = Product.wishlisted.all()
    return render(request, 'store/collections.html',{'products':products})


def add_item(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        try:
            product_id = int(request.POST.get('productid'))
        except:
            print('an error occured here')

        product = get_object_or_404(Product, id=product_id)
        if product.is_wishlisted:
            product.is_wishlisted = False
            product.save()
        else:
            product.is_wishlisted = True
            product.save() 
        # x = basket.wishlist(product,product_id)
        x = product.is_wishlisted
        print(product.is_wishlisted)
        response = JsonResponse({'status': x})
        return response