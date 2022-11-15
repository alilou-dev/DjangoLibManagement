from django.urls import path 
from django.contrib import admin
from main import views

urlpatterns = [
    path('register/', views.register, name="sign_up"),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
]
