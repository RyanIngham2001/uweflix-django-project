# Generated by Django 4.1.5 on 2023-04-23 16:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cinema", "0014_showing_social_distancing_seat"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="showing",
            name="adult_price",
        ),
        migrations.RemoveField(
            model_name="showing",
            name="child_price",
        ),
        migrations.RemoveField(
            model_name="showing",
            name="student_price",
        ),
    ]
