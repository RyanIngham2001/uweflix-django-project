# Generated by Django 4.1.7 on 2023-03-29 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0010_remove_ticket_priceid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='productID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
