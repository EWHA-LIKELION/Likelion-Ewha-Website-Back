from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(
        unique=True,
        error_messages={'unique': "A user with that email already exists."}
    )
    username = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.email
