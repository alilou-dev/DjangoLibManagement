from cgitb import html
from django.contrib import messages
from django.shortcuts import render, redirect
from main.form import AccountCreationForm
from django.contrib.auth.models import User
from Account import models
from main.templates.registration import *
# Create your views here.

def createAccount(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)    
        if form.is_valid():
            models.Account.objects.create(
                user = request.user,
                fisrtName = request.POST['firstName'],
                lastName = request.POST['lastName'],
                birthday = request.POST['birthday'],
                adress = request.POST['adress'],
                zipCode = request.POST['zipCode'],
                city = request.POST['city'],
                accountType = request.POST['accountType'],
            )
            return redirect("/home")
    else : 
        form = AccountCreationForm()        
    return render(request, 'accountCreate.html' ,{'form': form})
        
            