# Generated by Django 4.1.5 on 2023-04-16 21:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0003_user_account"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="discount_rate",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
