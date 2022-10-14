from django.shortcuts import render
from multiprocessing import context

# Create your views here.

def home(request):
    return render(request, './main/home.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')
