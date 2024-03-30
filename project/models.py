from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from technology.models import Tech
from custom_account.models import CustomUser


class Project(models.Model):
    """
    The project model. Projects have a one to many relationship
    with the user model. A user can have many projects, but
    a project can only have one user (for now).
    """
    user = models.ForeignKey(
        "custom_account.CustomUser",
        on_delete=models.CASCADE,
        related_name="projects")
    contributors = models.ManyToManyField("custom_account.CustomUser")
    technologies = models.ManyToManyField(
        Tech, blank=True, related_name="projects")
    name = models.CharField(max_length=100, blank=False, null=False)
    github_repo_url = models.URLField(max_length=255, blank=True, null=True)
    deployed_url = models.URLField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True, max_length=1000)
    image = CloudinaryField('image', blank=True, null=True)
    view_count = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        """
        Meta class for the project model.
        """
        ordering = ["-date_created"]
        unique_together = ["user", "name"]

    def __str__(self):
        """
        Returns the project name as a string.
        """
        return str(self.name)

    def num_view_count(self):
        """
        Returns the number of views a project has.
        """
        return self.view_count

    def get_absolute_url(self):
        """
        Returns the absolute url for a project.
        """
        return reverse(
            "project:view_project",
            kwargs={
                "slug": self.user.slug,
                "project_slug": self.slug})

    def delete(self, *args, **kwargs):
        """
        Override the delete method to delete the project's image from
        Cloudinary before deleting the project from the database.
        """
        if self.image:
            try:
                cloudinary.uploader.destroy(
                    self.image.public_id, invalidate=True)
            except Exception as e:
                print(f"Error deleting image from Cloudinary: {e}")

        super().delete(*args, **kwargs)

    def clean(self):
        if self.description and len(self.description) > 1000:
            raise ValidationError(
                {
                    'description':
                    'Description must be fewer than 1000 characters.'
                })

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a slug if one doesn't
        already exist and update the user's tech profile with approved
        technologies.
        """
        try:
            if self.user:
                pass
        except CustomUser.DoesNotExist:
            raise IntegrityError(
                "Only registered users can create projects.")

        if not hasattr(self.user, 'tech_profile'):
            raise IntegrityError(
                "Only Tech Users can create projects.")

        if not self.slug:
            self.slug = slugify(self.name)

        super(Project, self).save(*args, **kwargs)

        # This updates the tech on the tech user - requires a signal
        # to run after many to many update
        if self.user.tech_profile:
            self.user.tech_profile.update_tech_with_approved()
