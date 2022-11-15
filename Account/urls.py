from django.urls import path 
from Account import views

urlpatterns = [
    path('create/', views.createAccount, name="accountCreation"),
]

