from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail

from orders.views import user_orders

from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from .token import account_activation_token


@login_required
def dashboard(request):
    orders = user_orders(request)
    accounts = UserBase.objects.filter(is_active=True)
    return render(request,
                  'account/user/dashboard.html',
                  {'section': 'profile', 'orders': orders,'account':accounts})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/user/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):
    print('hello')

    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return redirect('account:registration_done')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')

def registration_done(request):
    return render(request,'account/registration/registration_done.html')

@login_required
def subscribe(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_subscribed = True
    user.save()
    email = request.POST.get('email')
    purpose = request.POST.get('purpose')
    print(email)
    print(purpose)
    try:
        if purpose =='sale10%':
            send_mail(subject='Subscription confirmation', message='Thanks for subscribing. \n \n \n You are now elligible for 10 percent off on all of our products. \n \n \n Thank You, \n Modern Classics',from_email='rockykhairnar2099@gmail.com',recipient_list=[email,])
            answer = 'Email sent'
        
        if purpose == 'new-arrival':
            print('yahan tak to aaya')
            send_mail(subject='Subscription confirmation', message='Thanks for subscribing. \n \n \n we will let you know  about our new products at the earliest.\n \n \n Thank You, \n Modern Classics',from_email='rockykhairnar2099@gmail.com',recipient_list=[email,])
            answer = 'Email sent'
    
    except:
        print(answer)
        answer = 'Please provide email in the correct format'
    response = JsonResponse({'success': answer})
    return response