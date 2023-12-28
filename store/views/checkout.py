from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from Eshop import settings
from store.models.product import Products
from store.models.orders import Order
from store.views.signal import send_order_notification
from twilio.rest import Client
from django.conf import settings
import os
import random
class CheckOut(View):
    def post(self, request):
        print("Working")
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                      product=product,
                      price=product.price,
                      address=address,
                      phone=phone,
                      quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}
        # send_order_notification(sender=Order, instance=order, created=True)
        return redirect('cart')
        # Proceed with pay on delivery
        
        # handle_google_pay()
        # return render(request, 'payment_gateway.html')

class ChoosePaymentMethod(View):
    def get(self, request):
        return render(request, 'choose_payment_method.html')

    def post(self, request):
        payment_method = request.POST.get('payment_method')
        request.session['payment_method'] = payment_method

        if payment_method == 'pay_on_delivery':
            return redirect('process_payment')
        else:
            return render(request, 'payment_gateway.html')
