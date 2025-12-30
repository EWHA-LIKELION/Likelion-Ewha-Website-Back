from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False
    ) 
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    def __str__ (self):
        return self.email