from django.db import models
from accounts.models import Account, PaymentDetails
from django.conf import settings

# Create your models here.

class PaymentReceipt(models.Model):
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name="account_receipt")
    payment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_of_payment")
    payment_card_details = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE, related_name="payment_card_details")
    required_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)