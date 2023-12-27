import pyotp

totp = pyotp.TOTP(pyotp.random_base32())
secret_key = totp.secret
print("Secret Key:", secret_key)
from django_otp.plugins.otp_totp.models import TOTPDevice
from pyotp import TOTP
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
from django.conf import settings
from twilio.rest import Client
import secrets
from store.models.customer import Customer
from store.models.product import Products
from store.models.orders import Order
from store.views.signal import send_order_notification

def random_hex(length=6):
    return secrets.token_hex(length)

def send_otp_via_sms(phone_number, otp_secret):
    # Replace the following with your Twilio credentials
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'Your OTP is: {otp_secret}',
        from_=twilio_phone_number,
        to=str(phone_number),
    )

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')

        # Check if the request is for OTP generation
        if not otp:
            # Generate OTP
            otp_secret = random_hex()
            totp_device = TOTPDevice(key=otp_secret, step=300, t0=0, confirmed=True)
            totp_device.save()

            # Send OTP via SMS
            send_otp_via_sms(phone, totp_device.token())

            return JsonResponse({'status': 'success', 'message': 'OTP sent successfully'})

        # Verify OTP
        if verify_otp(phone, otp):
            # Your existing code for processing the checkout
            address = request.POST.get('address')
            phone = request.POST.get('phone')

            payment_method = request.POST.get('payment_method')
            request.session['delivery_details'] = {'address': address, 'phone': phone}
            request.session['payment_method'] = payment_method

            if payment_method == 'pay_on_delivery':
                customer = request.session.get('customer')
                cart = request.session.get('cart')
                products = Products.get_products_by_id(list(cart.keys()))
                for product in products:
                    order = Order(customer=Customer(id=customer),
                                  product=product,
                                  price=product.price,
                                  address=address,
                                  phone=phone,
                                  quantity=cart.get(str(product.id)))
                    order.save()
                request.session['cart'] = {}
                return JsonResponse({'status': 'success', 'message': 'Order placed successfully'})
            elif payment_method == 'card':
                return JsonResponse({'status': 'success', 'message': 'Payment successful'})
            elif payment_method == 'googlepay':
                return JsonResponse({'status': 'success', 'message': 'Google Pay payment successful'})
            else:
                return JsonResponse({'status': 'success', 'message': 'Payment successful'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Incorrect OTP. Please try again.'})

def verify_otp(phone, otp):
    # Implement your OTP verification logic here
    # You can use a library like pyotp to generate and verify OTP
    # Example:
    totp_device = TOTPDevice.objects.filter(confirmed=True).last()
    return totp_device.verify(otp)
# views.py

from django_otp.plugins.otp_totp.models import TOTPDevice
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
from django.conf import settings
from twilio.rest import Client
import secrets
from store.models.customer import Customer
from store.models.product import Products
from store.models.orders import Order
import os
import json

def random_hex(length=6):
    return secrets.token_hex(length)

def send_otp_via_sms(phone_number, otp_secret):
    # Replace the following with your Twilio credentials
    account_sid = "AC1adf95b9101cc408a509bf5c08b8b2ea"
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    verify_sid = "VAb26a8e5ee4c5d49c12809f6a031cf924"
    verified_number = "+916006561669"

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=f'Your OTP is: {otp_secret}',
            from_=verified_number,
            to=str(phone_number),
        )
        return True
    except Exception as e:
        print(f"Error sending OTP: {str(e)}")
        return False

class CheckOut(View):
    template_name = 'cart.html'

    def get(self, request):
        products = Products.objects.filter(id__in=request.session.get('cart', {}).keys())
        return render(request, self.template_name, {'products': products})

    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')

        # Check if the request is for OTP generation
        if not otp:
            # Generate OTP
            otp_secret = random_hex()

            # Store the OTP secret in the session to verify later
            request.session['checkout_otp_secret'] = otp_secret
            request.session.modified = True  # Ensure the session is saved

            # Send OTP via SMS
            if send_otp_via_sms(phone, otp_secret):
                return JsonResponse({'status': 'success', 'message': 'OTP sent successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to send OTP'})

        # Verify OTP during checkout
        expected_otp_secret = request.session.get('checkout_otp_secret')

        if expected_otp_secret:
            totp_device = TOTPDevice(key=expected_otp_secret, step=300, t0=0, confirmed=True)

            try:
                # Print expected and entered OTP for debugging
                print(f"Expected OTP: {totp_device.token()}")
                print(f"Entered OTP: {otp}")

                # Verify the OTP token
                is_valid = totp_device.verify_token(otp)
                if is_valid:
                    # Your existing code for processing the checkout
                    address = request.POST.get('address')
                    phone = request.POST.get('phone')

                    payment_method = request.POST.get('payment_method')
                    request.session['delivery_details'] = {'address': address, 'phone': phone}
                    request.session['payment_method'] = payment_method

                    if payment_method == 'pay_on_delivery':
                        customer = request.session.get('customer')
                        cart = request.session.get('cart')
                        products = Products.get_products_by_id(list(cart.keys()))
                        for product in products:
                            order = Order(customer=Customer(id=customer),
                                          product=product,
                                          price=product.price,
                                          address=address,
                                          phone=phone,
                                          quantity=cart.get(str(product.id)))
                            order.save()
                        request.session['cart'] = {}
                        return JsonResponse({'status': 'success', 'message': 'Order placed successfully'})
                    elif payment_method == 'card':
                        return JsonResponse({'status': 'success', 'message': 'Payment successful'})
                    elif payment_method == 'googlepay':
                        return JsonResponse({'status': 'success', 'message': 'Google Pay payment successful'})
                    else:
                        return JsonResponse({'status': 'success', 'message': 'Payment successful'})
                else:
                    print("Error: Invalid OTP token.")
                    return JsonResponse({'status': 'error', 'message': 'Incorrect OTP. Please try again.'})
            except Exception as e:
                print(f"Error verifying OTP: {str(e)}")
                return JsonResponse({'status': 'error', 'message': 'Error verifying OTP. Please try again.'})
        else:
            print("Error: OTP secret not found in session.")
            return JsonResponse({'status': 'error', 'message': 'OTP secret not found. Please try again.'})


def verify_checkout_otp(request):
    # Retrieve the OTP secret and other necessary values stored in the session
    expected_otp_secret = request.session.get('checkout_otp_secret')
    phone = request.POST.get('phone')  # Retrieve 'phone' from POST data
    entered_otp = request.POST.get('otp')  # Retrieve 'otp' from POST data

    if expected_otp_secret is None:
        print("Error: OTP secret not found in session.")
        return JsonResponse({'status': 'error', 'message': 'OTP secret not found in session.'})

    totp_device = TOTPDevice(key=expected_otp_secret, step=300, t0=0, confirmed=True)

    if totp_device.key is None:
        print("Error: TOTPDevice key is None.")
        return JsonResponse({'status': 'error', 'message': 'TOTPDevice key is None.'})

    try:
        # Print expected and entered OTP for debugging
        print(f"Expected OTP: {totp_device.token()}")
        print(f"Entered OTP: {entered_otp}")

        # Verify the OTP token
        is_valid = totp_device.verify_token(entered_otp)
        if is_valid:
            return JsonResponse({'status': 'success', 'message': 'OTP verified successfully'})
        else:
            print("Error: Invalid OTP token.")
            return JsonResponse({'status': 'error', 'message': 'Invalid OTP token.'})
    except Exception as e:
        print(f"Error verifying OTP: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error verifying OTP.'})
