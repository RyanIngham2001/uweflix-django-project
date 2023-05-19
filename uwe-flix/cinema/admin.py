from django.contrib import admin
from django.apps import apps
from.models import Showing,Cinema

# Register your models here.
admin.site.register(Showing)
admin.site.register(Cinema)