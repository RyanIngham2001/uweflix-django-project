# Generated by Django 4.1.5 on 2023-03-22 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("clubs", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
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
