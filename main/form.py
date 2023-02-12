from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from Account.models import Account, Book, Operation, ReadingGroup
from django.core.validators import RegexValidator

class RegisterForm(UserCreationForm):
  # Set up form extra fields registration
  email = forms.EmailField(required=True)

  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):

  class Meta:
    model = User
    field = ["username", "password"]

class AccountCreationForm(forms.Form):
  phone_number_validator = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Format Incorrect ex : +6591258565")
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
  phone_number = forms.CharField(max_length=15, required=True)

  class Meta:
    model = Account
    fields = ["firstName","lastName","birthday","accountType","adress","zipCode","city","phone_number"]

class BookCreationForm(forms.Form):
  categories = [
    ('dv','diversifié'),
    ('dr','dramatique'),
    ('su','suspense'),
    ('na','naratif'),
    ('ac','action'),
    ('sc','science'),
    ('o','others')
  ]
  groups = [
    ('',''),
    ('',''),
  ]
  title = forms.CharField(required=True, max_length = 100)
  editor = forms.CharField(required=True, max_length = 20)
  shortDescription = forms.CharField(required=True, max_length = 1000)
  resume = forms.CharField(required=True, max_length=3000)
  quantity = forms.IntegerField()
  price = forms.DecimalField(max_digits = 5, decimal_places = 2)
  release_date = forms.DateField()
  category = forms.ChoiceField(
    required = True,
    choices = categories,
  )
  img = forms.ImageField(required=False)

  class Meta:
    model = Book
    fields = ["title","editor","shortDescription","resume","quantity","release_date","category","img"]

class RequestForBookForm(forms.Form):
  adress = forms.CharField(max_length=200, required=True)
  quantity = forms.IntegerField(min_value=1, required=True)
  amount = forms.DecimalField(max_digits = 5, decimal_places = 2, required=True)
  period_rental = forms.IntegerField(max_value=90, required=True)

  class Meta:
    model = Operation
    fields = ["adress","quantity","amount","period_rental"]

class ChallengeRequestForm(forms.Form):
  adress = forms.CharField(required=False, max_length=200)
  quantity = forms.IntegerField(min_value=1, required=False)
  amount = forms.DecimalField(max_digits = 5, decimal_places = 2, required=False)
  period_rental = forms.IntegerField(max_value=90, required=False)

  class Meta:
    model = Operation
    fields = ["adress","quantity","amount","period_rental"]

class ManageBookForm(forms.Form):
  categories = [
    ('',''),
    ('dv','diversifié'),
    ('dr','dramatique'),
    ('su','suspense'),
    ('na','naratif'),
    ('ac','action'),
    ('sc','science'),
    ('o','others'),
  ]
  newTitle = forms.CharField(required = False, max_length= 100)
  newEditor = forms.CharField(required= False, max_length= 20)
  newQuantity = forms.IntegerField(required= False)
  newPrice = forms.DecimalField(required = False,max_digits = 5, decimal_places = 2)
  newCategory = forms.ChoiceField(
    required = False,
    choices = categories,
  )
  newImg = forms.ImageField(required=False)

  class Meta:
    model = Book
    fields = ["newTitle","newEditor","newQuantity","newPrice","newCategory","newImg"]

class AddReadingGroupForm(forms.Form):
  name = forms.CharField(required=True, max_length=20)
  img = forms.ImageField(required=False)
  adress = forms.CharField(required=True, max_length=200)
  zipCode = forms.IntegerField(required=True, max_value=99999)
  city = forms.CharField(required=True, max_length=20)
  eventDate = forms.DateField()
  eventMoment = forms.TimeField(required=True)

  class Meta:
    model = ReadingGroup
    fields = ["name", "img", "adress", "zipCode", "city", "eventDate", "eventMoment"]