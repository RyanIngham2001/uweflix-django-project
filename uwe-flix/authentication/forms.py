from django import forms
from django.contrib.auth.models import User, Group
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "date_of_birth",
            "password1",
            "password2",
        )


class ElevateUserForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all().filter(is_rep=False))
    group = forms.ChoiceField(
        choices=[
            ("account_manager", "Account Manager"),
            ("cinema_manager", "Cinema Manager"),
            ("cinema_manager_temp", "Cinema Manager (Temporary)"),
            ("admin", "Admin"),
        ]
    )

    class Meta:
        model = User
        fields = ["user", "group"]
