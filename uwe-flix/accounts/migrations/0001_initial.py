# Generated by Django 4.1.5 on 2023-03-18 01:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("discount_rate", models.DecimalField(decimal_places=2, max_digits=5)),
                ("balance", models.DecimalField(decimal_places=2, max_digits=9)),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="PaymentDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("details_name", models.CharField(max_length=32)),
                ("payment_card_number", models.CharField(max_length=20)),
                ("payment_card_expiry_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="EndOfMonthStatement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(default=datetime.date.today)),
                ("total_spent", models.DecimalField(decimal_places=2, max_digits=10)),
                ("total_paid", models.DecimalField(decimal_places=2, max_digits=10)),
                ("outstanding", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="eom_account",
                        to="accounts.account",
                    ),
                ),
            ],
        ),
    ]