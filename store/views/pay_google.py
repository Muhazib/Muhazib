from django.shortcuts import render
from django.http import JsonResponse
def google_pay_request(request):
    # Your logic to generate payment data goes here
    payment_data = {
        'apiVersion': 2,
        'apiVersionMinor': 0,
    # Add other necessary parameters as per your requirements
    }
    return JsonResponse(payment_data)