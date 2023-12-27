from django.shortcuts import render , redirect

from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import  View
from store.models.product import Products

class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'products' : products} )
class RemoveFromCart(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        if product_id:
            cart = request.session.get('cart', {})
            if product_id in cart:
                del cart[product_id]
                request.session['cart'] = cart
                request.session.modified = True
        return redirect('cart')
class UpdateQuantity(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        if product_id and quantity > 0:
            cart = request.session.get('cart', {})
            cart[product_id] = quantity
            request.session['cart'] = cart
            request.session.modified = True
        return redirect('cart')
