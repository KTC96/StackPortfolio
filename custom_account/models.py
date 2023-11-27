from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from technology.models import Tech
from work_location_type.models import WorkLocationType


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
        if not email:
            raise ValueError('Users must have an email address.')

        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('Invalid email format.')

        if not 5 <= len(username) <= 20:
            raise ValueError('Username must be between 5 and 20 characters.')

        if not username.isalnum():
            raise ValueError('Username should not contain symbols.')

        if not 2 <= len(first_name) <= 40:
            raise TypeError('First name must be between 2 and 40 characters.')

        if not 2 <= len(last_name) <= 40:
            raise TypeError('Last name must be between 2 and 40 characters.')

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
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(
        max_length=20, unique=True, blank=False, null=False)
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

    def get_full_name(self):
        """
        Return the full name of a user.
        """
        return f'{self.first_name} {self.last_name}'

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
    technologies = models.ManyToManyField(Tech)
    work_location_type = models.ManyToManyField(
        WorkLocationType, default=1, blank=False)
    github_username = models.CharField(max_length=40, blank=True, null=True)
    seeking_employment = models.BooleanField(default=False)

    def update_tech_with_approved(self):
        """
        Update the tech profile to include only approved technologies
        from the user's projects.
        """
        approved_project_techs = Tech.objects.filter(
            projects__user=self.user, is_approved=True).distinct()

        # Add new approved techs and remove unapproved or old techs
        current_techs = set(self.technologies.all())

        for tech in approved_project_techs:
            if tech not in current_techs:
                self.technologies.add(tech)

        for tech in current_techs:
            if tech not in approved_project_techs:
                self.technologies.remove(tech)


class RecruiterUserProfile(models.Model):
    """
    The recruiter user profile model.
    """
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
