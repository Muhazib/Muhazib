from django.db import models

class Address(models.Model):
    pincode = models.CharField(max_length=10)
    area = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    alt_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
