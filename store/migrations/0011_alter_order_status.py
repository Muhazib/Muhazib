# Generated by Django 5.0 on 2023-12-15 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_order_is_phone_verified_order_otp_secret_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('Completed', 'Completed'), ('not available', 'Not Available'), ('cannot diliver right now', 'Cannot Dilever right now'), ('arriving', 'Arriving')], default='pending', max_length=50),
        ),
    ]