from django import forms
from .models import Account, EndOfMonthStatement, StudentDiscountRequest
from clubs.models import Club


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["discount_rate"]


class EndOfMonthStatementForm(forms.ModelForm):
    class Meta:
        model = EndOfMonthStatement
        fields = ["date", "total_spent", "total_paid", "outstanding"]


class TopUpForm(forms.Form):
    amount = forms.DecimalField(
        label="Top-Up Amount", decimal_places=2, min_value=0, required=True
    )


class StudentDiscountForm(forms.ModelForm):
    class Meta:
        model = StudentDiscountRequest
        fields = ["new_discount_rate", "reason"]
