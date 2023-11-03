from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class ParentUser(AbstractBaseUser):
    """
    Create a custom user model that uses
    Django's User model as a base.
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=40, blank=False, null=False)
    last_name = models.CharField(max_length=40, blank=False, null=False)

    USERNAME_FIELD = 'email'