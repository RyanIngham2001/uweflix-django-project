# Generated by Django 4.1.7 on 2023-05-01 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_account_stripecustomerid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='stripeCustomerID',
            field=models.CharField(default='TBD', max_length=255),
        ),
    ]
