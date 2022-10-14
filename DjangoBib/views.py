from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def loginPage(request):
    context = {}
    return render(request, './templates/login.html', context)

def registerPage(request):
    form = UserCreationForm()
    context = {'form': form}
    return render(request, './templates/register.html', context)    
