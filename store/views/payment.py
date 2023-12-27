from django.shortcuts import render
from django.views import View
import stripe
from django.conf import settings

class PaymentIntentView(View):
    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        amount = 1000  # Amount in cents
        currency = 'usd'

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
        )

        client_secret = intent.client_secret

        return render(request, 'payment_gateway.html', {'client_secret': client_secret})
