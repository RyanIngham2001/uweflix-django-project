# Generated by Django 4.1.5 on 2023-03-17 01:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cinema", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seat",
            name="reserved",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="seat_reserved",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
