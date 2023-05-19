# Generated by Django 4.1.5 on 2023-05-03 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Club",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("street_number", models.IntegerField()),
                ("street", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("postcode", models.CharField(max_length=255)),
                ("telephone_number", models.CharField(max_length=255)),
                ("mobile_number", models.CharField(max_length=255)),
                ("email_address", models.EmailField(max_length=255)),
                ("active", models.BooleanField(default=False)),
                (
                    "account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="club_account",
                        to="accounts.account",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ClubRepresentative",
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
                ("representative_id", models.CharField(max_length=50, unique=True)),
                ("email", models.EmailField(max_length=255, null=True)),
                ("first_name", models.CharField(max_length=255, null=True)),
                ("last_name", models.CharField(max_length=255, null=True)),
                ("password", models.CharField(max_length=255, null=True)),
                (
                    "linked_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ClubDiscountRequest",
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
                ("old_discount_rate", models.FloatField(default=0)),
                ("new_discount_rate", models.FloatField(default=0)),
                ("reason", models.CharField(max_length=255)),
                ("approved", models.BooleanField(default=False)),
                (
                    "club",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="discount_requests",
                        to="clubs.club",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="club",
            name="representative",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="clubs",
                to="clubs.clubrepresentative",
            ),
        ),
    ]
