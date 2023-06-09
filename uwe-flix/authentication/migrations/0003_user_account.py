# Generated by Django 4.1.5 on 2023-03-23 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_cinemaaccount_useraccount"),
        ("authentication", "0002_delete_clubrepresentative"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="account",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="accounts",
                to="accounts.useraccount",
            ),
        ),
    ]
