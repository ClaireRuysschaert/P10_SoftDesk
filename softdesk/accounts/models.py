from datetime import timezone
import datetime
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
    We calculate the user's age and if it is less than 15, the can_be_contacted and can_be_shared fields are set to False.

    Overrides the save method to enforce the age restriction.

    """

    birthdate = models.DateField()
    updated_on = models.DateTimeField(auto_now=True)
    can_be_contacted = models.BooleanField(default=True)
    can_be_shared = models.BooleanField(default=True)

    REQUIRED_FIELDS = ["email", "birthdate"]

    def save(self, *args, **kwargs):
        today = datetime.date.today()
        age = (today - self.birthdate) // datetime.timedelta(days=365.2425)
        if age < 15:
            self.can_be_contacted = False
            self.can_be_shared = False
        super().save(*args, **kwargs)
