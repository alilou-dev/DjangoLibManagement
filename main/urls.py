from django.urls import path 
from django.contrib import admin
from main import views

urlpatterns = [
    path('home/', views.home),
    path('login/', views.login),
    path('register/', views.register),
    path('admin/', admin.site.urls)
]
