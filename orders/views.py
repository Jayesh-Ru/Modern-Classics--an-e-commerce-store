from django.http.response import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from basket.basket import Basket

from .models import Order, OrderItem
from django.core.mail import send_mail


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        order_key = request.POST.get('order_key')
        user_id = request.user.id
        email = request.user.email
        print(email)
        name = request.POST.get('full_name')
        add1 = request.POST.get('add1')
        add2 = request.POST.get('add2')
        country = request.POST.get('country')
        postcode = request.POST.get('postcode')
        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name=name, address1=add1,
                                address2=add2,phone='x',post_code=postcode,country=country, total_paid=baskettotal, order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])
            
            subject= 'Order confirmation'
            message= render_to_string('payment/order_confirmation.html', {
                'name': name,
                'address': add1,
                'country':country,
                'pincode':postcode,
            })
            send_mail(subject=subject, message=message,from_email='rockykhairnar2099@gmail.com',recipient_list=[email,])

        response = JsonResponse({'success': 'Return something'})
        return response

# def cancel(request):
#     basket = Basket(request)
#     if request.POST.get('action') == 'post':
#         order_key = request.POST.get('order_key')
#     if Order.objects.filter(order_key=order_key).exists():
#         order= Order.objects.filter(order_key=order_key)
        
#         subject= 'Order cancellation'
#         message= render_to_string('payment/order_cancellation.html', {
#                 'name': request.user.full_name,
#         })
#         send_mail(subject=subject, message=message,from_email='rockykhairnar2099@gmail.com',recipient_list=[email,])

#     response = JsonResponse({'success': 'Order cancelled'})
#     return response

def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)
    # orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders