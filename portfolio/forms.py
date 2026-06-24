from django import forms
from .models import Portfolio, Trade
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = [
            "name",
            "risk_limit"
        ]
   

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = [
            "symbol",
            "quantity",
            "price",
            "trade_type"
        ]


class RegisterForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]