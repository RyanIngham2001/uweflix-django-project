# Generated by Django 4.1.7 on 2023-04-26 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_clubaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentDiscountRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_discount_rate', models.FloatField(default=0)),
                ('new_discount_rate', models.FloatField(default=0)),
                ('reason', models.CharField(max_length=255)),
                ('approved', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='discount_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
