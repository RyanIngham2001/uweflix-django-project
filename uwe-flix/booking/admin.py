from django.contrib import admin
from django.apps import apps
from.models import Reservation,Cancelation
# Register your models here.
admin.site.register(Reservation)
admin.site.register(Cancelation)