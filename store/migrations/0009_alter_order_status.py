# Generated by Django 5.0 on 2023-12-13 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_carouselimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]