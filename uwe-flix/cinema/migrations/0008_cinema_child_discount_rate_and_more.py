# Generated by Django 4.1.5 on 2023-03-24 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0007_showing_avalible_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinema',
            name='child_discount_rate',
            field=models.FloatField(default=50.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cinema',
            name='student_discount_rate',
            field=models.FloatField(default=25.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cinema',
            name='ticket_price',
            field=models.FloatField(default=8.99),
            preserve_default=False,
        ),
    ]
