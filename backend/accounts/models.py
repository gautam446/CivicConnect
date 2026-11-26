from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (("citizen", "Citizen"), ("staff", "Staff"), ("admin", "Admin"))
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default="citizen")
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = "admin"
        super().save(*args, **kwargs)
