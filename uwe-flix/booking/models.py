from django.db import models
from cinema.models import Showing, Cinema, Ticket, Film
from django.conf import settings

# Create your models here.

#Model for reservations
class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE, related_name='showings')
    student_quantity = models.IntegerField(default=0)
    adult_quantity = models.IntegerField(default=0)
    child_quantity = models.IntegerField(default=0)
    booking_cost = models.FloatField()
    reservee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservees', default=None, null=True)
    guest_reservee = models.CharField(max_length=255, null=True)
    cancelled = models.BooleanField(default=None, blank=True, null=True)
    cancellation_requested = models.BooleanField(default=False, blank=False, null=False)
    reservee_email = models.EmailField(blank=True, null=True)

#Model for cancelations
class Cancelation(models.Model):
    id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='reservation')
    approved = models.BooleanField(default = None, blank= True, null=True)

class StripeInformation(object):
    def __init__(self, name, description, unit_amount, quantity):
        self.name = name
        self.description = description
        self.unit_amount = unit_amount
        self.quantity = quantity