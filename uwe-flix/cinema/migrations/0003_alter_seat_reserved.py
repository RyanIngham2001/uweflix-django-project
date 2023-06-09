# Generated by Django 4.1.5 on 2023-03-17 01:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cinema", "0002_alter_seat_reserved"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seat",
            name="reserved",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="seat_reserved",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
