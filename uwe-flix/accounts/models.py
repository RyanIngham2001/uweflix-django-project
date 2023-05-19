from django.db import models
import datetime
from django.conf import settings
# from payments.models import PaymentReceipt
# Create your models here.

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    balance = models.DecimalField(max_digits=9, decimal_places=2)
    name = models.CharField(max_length=255)
    stripeCustomerID = models.CharField(max_length=255, default="TBD")
    
    
class ClubAccount(Account):
    pass
    
    
class UserAccount(Account):
    pass


class CinemaAccount(Account):
    pass


class PaymentDetails(models.Model):
    details_name = models.CharField(max_length=32)
    payment_card_number = models.CharField(max_length=20)
    payment_card_expiry_date = models.DateField()


class EndOfMonthStatement(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="eom_account")
    date = models.DateField(default=datetime.date.today)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    outstanding = models.DecimalField(max_digits=10, decimal_places=2)

    def update_outstanding(statement_id):
        statement = EndOfMonthStatement.objects.get(pk=statement_id)
        return statement.total_spent - statement.total_paid
    

class StudentDiscountRequest(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='discount_requests')
    old_discount_rate = models.FloatField(default=0)
    new_discount_rate = models.FloatField(default=0)
    reason = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)


class TopUpStripeInformation(object):
    def __init__(self, name, description, unit_amount, quantity, customerID):
        self.name = name
        self.description = description
        self.unit_amount = unit_amount
        self.quantity = quantity
        self.customerID = customerID


class TransactionHistory(object):
    def __init__(self, transId, amount, created, status):
        self.transId = transId
        self.amount = amount
        self.created = created
        self.status = status
