from django import forms
from .models import Reservation,Showing
from cinema.forms import ShowingForm
from datetime import datetime

class ReservationForm(forms.ModelForm):
    showing = forms.ModelChoiceField(queryset=Showing.objects.none())
    
    class Meta:
        model = Reservation
        fields = ['showing','student_quantity','adult_quantity','child_quantity']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        current_time = datetime.now().replace(second=0, microsecond=0)
        self.fields['showing'].queryset = Showing.objects.filter(start_time__gte=current_time)
        if user.is_authenticated:
            if user.is_rep == True:
                self.fields['adult_quantity'].widget = forms.HiddenInput()
                self.fields['child_quantity'].widget = forms.HiddenInput()
                self.fields['student_quantity'].widget.attrs['min'] = 10
                self.fields['student_quantity'].initial = 10

class ReservationSearch(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['guest_reservee']