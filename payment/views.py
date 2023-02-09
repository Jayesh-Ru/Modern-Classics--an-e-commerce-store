import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from account.forms import OrderDetailsForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from basket.basket import Basket
from account.token import account_activation_token
from orders.views import payment_confirmation


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    template_name = 'payment/error.html'

# @login_required
# def OrderForm(request):


@login_required
def BasketView(request):
    orders = OrderDetailsForm()
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    stripe.api_key = 'sk_test_51MYZBdSDcRej9N7gQrQyYCOyoxGvcW6bmAsdgkUU7N8SWuKY25uu8UEY3zw3LwkKrnyTxhQ7HrjQX3O9f9suWpt2008Nlf5vt6'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='INR',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/home.html', {'client_secret': intent.client_secret,'form':orders})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

# def orderCancelled(request):
#     return HttpResponse(status = 200)

