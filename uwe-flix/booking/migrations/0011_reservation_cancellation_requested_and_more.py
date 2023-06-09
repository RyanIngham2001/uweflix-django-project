# Generated by Django 4.1.5 on 2023-05-05 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_alter_reservation_adult_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='cancellation_requested',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='cancelled',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
