# Generated by Django 4.1.5 on 2023-03-27 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_remove_reservation_a_remove_reservation_booking_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='booking_cost',
            field=models.FloatField(default=5.0),
            preserve_default=False,
        ),
    ]
