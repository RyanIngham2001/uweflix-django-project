from django.db import models
from django.conf import settings
from authentication.models import User
from accounts.models import Account
# Create your models here.
    
    
class ClubRepresentative(models.Model):
    linked_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user', null=False, blank=False)
    representative_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    
    
class Club(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    representative = models.ForeignKey(
        ClubRepresentative,
        on_delete=models.CASCADE,
        related_name='clubs',
        null=True,
        blank=True
    )
    street_number = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    telephone_number = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=255)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='club_account',
        null=True,
        blank=True
    )
    active = models.BooleanField(default=False)
    
class ClubDiscountRequest(models.Model):
    club = models.ForeignKey(Club, on_delete=models.PROTECT, related_name='discount_requests')
    old_discount_rate = models.FloatField(default=0)
    new_discount_rate = models.FloatField(default=0)
    reason = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)