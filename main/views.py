import email
from email import message
from django.shortcuts import render, redirect
from multiprocessing import context
from .form import RegisterForm
from django.contrib.auth import login as login_process, logout, authenticate
from django.contrib import messages
from Account import views

from main import form

# here we use the tag login_process because of def login there is after (conflit between them)

# Create your views here.

def home(request):
    return render(request, 'shared/home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,user)
        if user is not None:
            login_process(request, user)
            return redirect('/home')
        else : 
            return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)   
        if form.is_valid():
            user = form.save()
            login_process(request, user)
            return redirect(views.createAccount)
            
    else :
        form = RegisterForm()    
    
    return render(request, 'registration/sign_up.html', {"form": form})
    

