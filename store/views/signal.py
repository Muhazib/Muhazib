# signals.py

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from store.models.orders import Order
@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, **kwargs):
    if kwargs.get('created', False):  # Only trigger for new orders
        subject = 'New Order Notification'
        message = render_to_string('order_notification_email.html', {'order': instance})
        plain_message = strip_tags(message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = 'nuzhatshah30@gmail.com'  # Replace with your admin's email address
        send_mail(subject, plain_message, from_email, [to_email], html_message=message)
@receiver(pre_delete, sender=Order)
def send_order_cancellation_notification(sender, instance, **kwargs):
    subject = 'Order Cancellation Notification'
    message = render_to_string('order_cancellation_notification_email.html', {'order': instance})
    plain_message = strip_tags(message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = 'nuzhatshah30@gmail.com'  # Replace with your admin's email address
    send_mail(subject, plain_message, from_email, [to_email], html_message=message)
