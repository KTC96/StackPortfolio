from django.db import models


class WorkLocationType(models.Model):
    """
    The Work Location Model is a many to many model for
    the CustomUser and the Job Post model. A user can choose
    their work location preference (on site, hybrid, remote)
    and a job post can specify which work location they are
    offering.
    """
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name
