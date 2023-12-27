from django.contrib import admin
from django.urls import path
from .views.home import Index , store, home
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart,RemoveFromCart,UpdateQuantity
from .views.checkout import CheckOut
from .views.orders import OrderView,CancelOrderView
from .views.payment import PaymentIntentView
from .middlewares.auth import  auth_middleware
from .views.pay_google import google_pay_request
from .views.adress import save_address
urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('home/', home, name='homee'),
    path('store', store , name='store'),
    path('signup/', Signup.as_view(), name='signup'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('remove_from_cart/', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('update_quantity/', UpdateQuantity.as_view(), name='update_quantity'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('address/', save_address, name='save_address'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('cancel-order/<int:order_id>/', CancelOrderView.as_view(), name='cancel_order'),
    path('google-pay-request/', google_pay_request, name='google_pay_request'),
    path('payment-intent/', PaymentIntentView.as_view(), name='payment_intent'),
]
