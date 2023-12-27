from django.db import models
from .product import Products
from .customer import Customer
import datetime


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE)
    product_name = Products.name
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField (max_length=50, default='', blank=True)
    phone = models.CharField (max_length=10, default='9598372834', blank=True)
    # otp_secret = models.CharField(max_length=16)  # Store the OTP secret key
    # is_phone_verified = models.BooleanField(default=False)
    date = models.DateField (default=datetime.datetime.today)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('Completed', 'Completed'),
        ('no available', 'Not Available'),
        ("cannot diliver right now", "Cannot Dilever right now"),
        ("arriving", "Arriving")
    ]

    # status = models.NullBooleanField(choices=STATUS_CHOICES, default=False)
    # status = models.BooleanField (default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
    def __str__(self):
        return f"Order {self.id} - {self.product.name} by {self.customer.first_name}"
