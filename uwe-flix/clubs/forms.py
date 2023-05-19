from django import forms
from .models import Club, ClubRepresentative, ClubDiscountRequest

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'street_number', 'street', 'city', 'postcode', 'telephone_number', 'mobile_number', 'email_address']
        

class ClubRepresentativeForm(forms.ModelForm):
    class Meta:
        model = ClubRepresentative
        fields = ['email', 'first_name', 'last_name', 'password']
    
class ClubDiscountRequestForm(forms.ModelForm):
    class Meta:
        model = ClubDiscountRequest
        fields = ['new_discount_rate', 'reason']