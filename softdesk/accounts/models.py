from django.contrib.auth.models import AbstractUser
from django.db import models


class SoftUser(AbstractUser):
    """
    Custom user model for Softdesk application.

    Inherits from AbstractUser and adds additional fields:
    - birthdate: DateField representing the user's birthdate.
    - updated_on: DateTimeField representing the last update timestamp.
    - can_be_contacted: BooleanField indicating if the user can be contacted.
    - can_be_shared: BooleanField indicating if the user's information can be shared.

    The birthdate field is required due to RGPD (General Data Protection Regulation).
    """

    email = models.EmailField()
    birthdate = models.DateField()
    updated_on = models.DateTimeField(auto_now=True)
    can_be_contacted = models.BooleanField(default=True)
    can_be_shared = models.BooleanField(default=True)


class Contributor(models.Model):
    user = models.ForeignKey(SoftUser, on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "project"]
        ordering = ["-date_joined"]
