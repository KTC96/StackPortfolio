from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from custom_account.models import CustomUser


class Project(models.Model):
    """
    The project model. Projects have a one to many relationship
    with the user model. A user can have many projects, but
    a project can only have one user (for now).
    """
    user = models.ForeignKey(
        "custom_account.CustomUser", on_delete=models.CASCADE, related_name="projects")
    project_name = models.CharField(max_length=100, blank=False, null=False)
    github_repo_url = models.URLField(max_length=255)
    deployed_url = models.URLField(max_length=255)
    project_active = models.BooleanField(default=True)
    project_description = models.TextField()
    project_image = CloudinaryField('image')
    project_view_count = models.IntegerField(default=0)
    project_slug = models.SlugField(blank=True, null=True)
    project_date_created = models.DateTimeField(auto_now_add=True)
    project_date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.project_name)

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a slug
        if one doesn't already exist.
        """
        if not self.project_slug:
            self.project_slug = slugify(self.project_name)
        super(Project, self).save(*args, **kwargs)
