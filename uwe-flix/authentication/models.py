from django.db import models
from django.contrib.auth.models import AbstractUser, Group
import datetime
from accounts.models import UserAccount

# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateField(default=datetime.date.today)
    discount_rate = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    is_rep = models.BooleanField(default=False)
    account = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="accounts", null=True
    )


class Group(Group):
    expiry_date = models.DateField(
        default=None,
        null=True,
    )
