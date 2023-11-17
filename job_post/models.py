from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from technology.models import Tech


class Project(models.Model):
    """
    The project model. Projects have a one to many relationship
    with the user model. A user can have many projects, but
    a project can only have one user (for now).
    """
    user = models.ForeignKey(
        "custom_account.CustomUser",
        on_delete=models.CASCADE,
        related_name="job_posts")
    technologies = models.ManyToManyField(
        Tech, blank=True, related_name="job_posts")
    name = models.CharField(max_length=100, blank=False, null=True)
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    view_count = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True,  null=True)
    date_updated = models.DateTimeField(auto_now=True,  null=True)

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

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a slug if one doesn't already exist
        and update the user's tech profile with approved technologies.
        """
        if not self.slug:
            self.slug = slugify(self.name)

        super(Project, self).save(*args, **kwargs)

        # This updates the tech on the tech user - requires a signal
        # to run after many to many update
        if self.user.tech_profile:
            self.user.tech_profile.update_tech_with_approved()
