from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


class CustomUserManager(BaseUserManager):
    """
    Create a custom user manager class that
    extends BaseUserManager.
    """

    def create_user(
            self,
            email,
            username,
            first_name,
            last_name,
            password=None,
            town_city=None,
            display_town_city=False,
            country=None,
            display_email=False,
            website=None,
            phone_number=None,
            display_phone_number=False,
            profile_image=None,
            bio=None,
            work_title=None,
            company=None,
            linkedin_username=None,
            twitter_handle=None,
    ):
        """
        Create and return a `CustomUser` with an email, username,
        first name, last name, and password.
        """
        if email is None:
            raise TypeError('Users must have an email address.')
        if username is None:
            raise TypeError('Users must have a username.')
        if first_name is None:
            raise TypeError('Users must have a first name.')
        if last_name is None:
            raise TypeError('Users must have a last name.')

        user = self.model(
            # normalize_email() is used to lowercase
            # the domain part of the email address.
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            town_city=town_city,
            display_town_city=display_town_city,
            country=country,
            display_email=display_email,
            website=website,
            phone_number=phone_number,
            display_phone_number=display_phone_number,
            profile_image=profile_image,
            bio=bio,
            work_title=work_title,
            company=company,
            linkedin_username=linkedin_username,
            twitter_handle=twitter_handle,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        email,
        username="default_username",
        first_name="default_firstname",
        last_name="default_lastname",
        password=None
    ):
        """
        Create and return a `CustomUser` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            email, username, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Create a custom user model that uses
    Django's User model as a base.
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=40, blank=False, null=False)
    last_name = models.CharField(max_length=40, blank=False, null=False)
    town_city = models.CharField(max_length=85, blank=True, null=True)
    display_town_city = models.BooleanField(default=False)
    country = models.CharField(max_length=60, blank=True, null=True)
    display_email = models.BooleanField(default=False)
    website = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    display_phone_number = models.BooleanField(default=False)
    profile_image = CloudinaryField(
        'image', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    work_title = models.CharField(max_length=80, blank=True, null=True)
    company = models.CharField(max_length=80, blank=True, null=True)
    linkedin_username = models.CharField(max_length=80, blank=True, null=True)
    twitter_handle = models.CharField(max_length=80, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class TechUserProfile(models.Model):
    """
    The tech user profile model.
    """
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='tech_profile')
    github_username = models.CharField(max_length=40, blank=True, null=True)
    seeking_employment = models.BooleanField(default=False)


class RecruiterUserProfile(models.Model):
    """
    The recruiter user profile model.
    """
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
