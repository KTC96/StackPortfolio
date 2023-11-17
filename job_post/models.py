from django.db import models
from django.urls import reverse
from technology.models import Tech


class JobPost(models.Model):
    """
    The Job Post model. Job posts have a one to many relationship
    with the user model. A user can have many job posts, but
    a job post can only have one user. Job posts are created by
    a recruiter user and viewed by anyone.
    """
    user = models.ForeignKey(
        "custom_account.CustomUser",
        on_delete=models.CASCADE,
        related_name="job_posts")
    technologies = models.ManyToManyField(
        Tech, blank=True, related_name="job_posts")
    name = models.CharField(max_length=100, blank=False,
                            null=True)  # Job title
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    view_count = models.IntegerField(default=0)
    company = models.CharField(max_length=80, blank=True, null=True)
    location = models.CharField(max_length=80, blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=3, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True,  null=True)
    date_updated = models.DateTimeField(auto_now=True,  null=True)

    class Meta:
        """
        Meta class for the job post model.
        """
        ordering = ["-date_created"]

    def __str__(self):
        """
        Returns the job post name as a string.
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
            "job_post:view_job_post",
            kwargs={
                "slug": self.user.slug,
                "id": self.id
            })

    def save(self, *args, **kwargs):
        """
        Saves the job post.
        """
        super(JobPost, self).save(*args, **kwargs)
