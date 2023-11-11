from django.db import models


class Tech(models.Model):
    """
    The tech model. Tech have a many to many relationship
    with the project and CustomUser models. A project can
    have many techs and a tech can have many projects. A
    user will have any tech that is associated with their
    projects.
    """
    tech_name = models.CharField(max_length=80, unique=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.tech_name
