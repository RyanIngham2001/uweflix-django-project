# Generated by Django 4.1.7 on 2023-05-04 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stripePayments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stripereceipt',
            name='charge',
        ),
        migrations.DeleteModel(
            name='StripeCharge',
        ),
        migrations.DeleteModel(
            name='StripeReceipt',
        ),
    ]
