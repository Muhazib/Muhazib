from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.models.orders import Order
from store.middlewares.auth import auth_middleware
class CancelOrderView(View):

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()  # Delete the order
        # You can also add logic here to notify the admin about the cancellation.
        return redirect('orders')
class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})
