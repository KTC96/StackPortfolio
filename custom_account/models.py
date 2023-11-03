from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class ParentUser(AbstractBaseUser):
    """
    Create a custom user model that uses
    Django's User model as a base.
    """
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'