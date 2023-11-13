from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from technology.models import Tech


class Project(models.Model):
    """
    The project model. Projects have a one to many relationship
    with the user model. A user can have many projects, but
    a project can only have one user (for now).
    """
    user = models.ForeignKey(
        "custom_account.CustomUser", on_delete=models.CASCADE, related_name="projects")
    technologies = models.ManyToManyField(
        Tech, blank=True, related_name="projects")
    project_name = models.CharField(max_length=100, blank=False, null=False)
    github_repo_url = models.URLField(max_length=255, blank=True, null=True)
    deployed_url = models.URLField(max_length=255, blank=True, null=True)
    project_active = models.BooleanField(default=True)
    project_description = models.TextField(blank=True, null=True)
    project_image = CloudinaryField('image', blank=True, null=True)
    project_view_count = models.IntegerField(default=0)
    project_slug = models.SlugField(blank=True, null=True)
    project_date_created = models.DateTimeField(auto_now_add=True)
    project_date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for the project model.
        """
        ordering = ["-project_date_created"]
        unique_together = ["user", "project_name"]

    def __str__(self):
        """
        Returns the project name as a string.
        """
        return str(self.project_name)

    def num_view_count(self):
        """
        Returns the number of views a project has.
        """
        return self.project_view_count

    def get_absolute_url(self):
        """
        Returns the absolute url for a project.
        """
        return reverse("project:view_project", kwargs={"slug": self.user.slug, "project_slug": self.project_slug})

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a slug
        if one doesn't already exist.
        """
        if not self.project_slug:
            self.project_slug = slugify(self.project_name)
        super(Project, self).save(*args, **kwargs)
