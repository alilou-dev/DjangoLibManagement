from dataclasses import field
from email.policy import default
from random import choices
from secrets import choice
from urllib import request
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main import models
from Account.models import Account

class RegisterForm(UserCreationForm):
    #set up form extra fields registration     
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
class AccountCreationForm(forms.Form):
    
    firstName = forms.CharField(required=True, max_length = 7)
    lastName = forms.CharField(required=True, max_length = 8)
    birthday = forms.DateField()
    accountType = forms.ChoiceField(
        choices=[
            ('lb', 'libraire'),
            ('cl', 'client')
        ],
    )
    adress = forms.CharField(max_length = 200, required=True)  
    zipCode = forms.CharField(max_length = 5, required=True)  
    city = forms.CharField(max_length = 20, required=True)
    class Meta:
        model = Account
        fields = ["firstName","lastName","birthday","accountType","adress","zipCode","city"]
            