from django import forms
from .models import Screen, Cinema, Showing, Film, Ticket


class ScreenForm(forms.ModelForm):
    cinema = forms.ModelChoiceField(queryset=Cinema.objects.all())

    class Meta:
        model = Screen
        fields = ['cinema', 'screen_number', 'seating_capacity']

class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = ['name', 'location']

class ShowingForm(forms.ModelForm):
    screen = forms.ModelChoiceField(queryset=Screen.objects.all().order_by('screen_number'))
    film = forms.ModelChoiceField(queryset=Film.objects.all().order_by('title'))
    class Meta:
        model = Showing
        fields = ['screen', 'film', 'start_time', 'social_distancing']

class FilmForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=Film.ageRatings)
    class Meta:
        model = Film
        fields = ['title', 'length', 'rating', 'description']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'price']