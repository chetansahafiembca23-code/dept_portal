from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    DEPT_CHOICES = (
        ('BCA', 'BCA'),
        ('MCA', 'MCA'),
        ('OTHER', 'Other Department'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    college_email = models.EmailField(blank=True)
    department = models.CharField(max_length=10, choices=DEPT_CHOICES, blank=True)

    # This boolean tells us if they have filled out the mandatory details
    is_profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"