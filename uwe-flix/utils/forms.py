from django import forms

class IndexForm(forms.Form):
    date = forms.DateField()