from email.policy import default
from time import timezone
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    fisrtName = models.CharField(max_length = 8, default='')
    lastName = models.CharField(max_length = 8, default = '')
    birthday = models.DateField(default = date.today)
    ACCOUNT_TYPE = (
        ('lb', 'libraire'),
        ('cl', 'client'),
    )
    accountType = models.CharField(
        max_length = 10,
        choices = ACCOUNT_TYPE,
        default = 'cl',
        
    )
    adress = models.CharField(max_length = 200, default = '')
    city = models.CharField(max_length = 20, default = '')
    zipCode = models.CharField(max_length = 5, default = '0000')
    
    
    def __str__(self):
        return self.user.username